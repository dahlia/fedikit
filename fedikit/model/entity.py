from asyncio import to_thread
from collections.abc import Iterable, Mapping, MutableSequence, Sequence
from typing import (
    Any,
    ClassVar,
    NewType,
    Optional,
    Self,
    TypeAlias,
    TypeVar,
    Union,
    cast,
    dataclass_transform,
    get_type_hints,
)

from pyld import jsonld
from pyld.documentloader.requests import requests_document_loader

from .converters import jsonld as to_jsonld
from .descriptors import Property, SingularProperty
from .docloader import DocumentLoader
from .scalars import ScalarValue

__all__ = ["Entity", "EntityRef", "Slot", "Uri", "load_entity_refs"]


Uri = NewType("Uri", str)


Slot: TypeAlias = (
    Uri | MutableSequence[Union["EntityRef", ScalarValue, "Entity"]]
)


@dataclass_transform(frozen_default=True, kw_only_default=True)
class Entity:
    """A base class for ActivityPub types.  Subclasses must define the
    :attr:`__uri__` and :attr:`__default_context__` class variables, and may
    define properties using the :func:`.descriptors.id_property()`,
    :func:`.descriptors.singular_property()`, and
    :func:`.descriptors.plural_property()`.
    """

    #: The URI of the type.
    __uri__: ClassVar[Uri]

    #: The default JSON-LD context for the type.  It is used when compacting
    #: the JSON-LD document.
    __default_context__: ClassVar[Uri | Sequence[Uri] | Mapping[str, Any]]

    _values: Mapping[Uri, Slot]
    __extra__: Mapping[Uri, Any]

    @classmethod
    async def __from_jsonld__(
        cls,
        document: Mapping[str, Any],
        loader: Optional[DocumentLoader] = None,
    ) -> Self:
        doc_loader = get_raw_document_loader(loader)
        doc = await to_thread(
            lambda: jsonld.expand(
                document,
                {"documentLoader": doc_loader},
            )[0]
        )
        if "@type" in doc:
            if cls is Entity or cls.__uri__ not in doc["@type"]:
                for doc_type in doc["@type"]:
                    entity_type = get_entity_type(Uri(doc_type))
                    if entity_type is not None and issubclass(
                        entity_type, cls
                    ):
                        return await entity_type.__from_jsonld__(doc)
                raise ValueError(
                    f"unsupported type: {doc['@type']!r}"
                    if cls is Entity
                    else f"expected type {cls.__uri__!r}, got {doc['@type']!r}"
                )
        values: dict[str, Any] = {}
        extra: dict[Uri, Any] = {}
        descriptors: Mapping[Uri, Mapping[str, Property]] = (
            get_uri_descriptors(cls)
        )
        type_hints = get_type_hints(cls)
        for uri, vals in doc.items():
            desc_dict = descriptors.get(Uri(uri), {})
            desc_kvs = list(desc_dict.items())
            # Give priority to plural properties over singular ones:
            desc_kvs.sort(key=lambda kv: isinstance(kv[1], SingularProperty))
            for name, desc in desc_kvs:
                try:
                    values[name] = await desc.parse_jsonld(
                        type_hints[name], vals
                    )
                except TypeError:
                    continue
                else:
                    break
            else:
                if uri != "@type":
                    extra[Uri(uri)] = vals
        instance = cls(**values, __extra__=extra)
        return instance

    def __init__(
        self,
        *,
        __extra__: Mapping[Uri, Any] = {},  # noqa: B006
        **kwargs: Mapping[str, Any],
    ) -> None:
        values: dict[Uri, Slot] = {}
        props: dict[Uri, str] = {}
        cls = type(self)
        for key, value in kwargs.items():
            desc = getattr(cls, key, None)
            if not isinstance(desc, Property):
                raise AttributeError(
                    f"{cls.__name__} has no property named {key!r}"
                )
            elif desc.uri in props:
                raise AttributeError(
                    f"{key!r} and {props[desc.uri]!r} cannot both be set at"
                    " once"
                )
            values[desc.uri] = desc.normalize(value)
            props[desc.uri] = key
        self._values = values
        self.__extra__ = dict(__extra__)

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        assert isinstance(other, Entity)
        return (
            self._values == other._values and self.__extra__ == other.__extra__
        )

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        values = list(self._values.items())
        values.sort(key=lambda kv: kv[0])
        hv = hash(type(self))
        for uri, slot in values:
            hv = (37 * hv & 0xFFFFFFFF) + hash(uri) & 0xFFFFFFFF
            if isinstance(slot, str):
                hv = (37 * hv & 0xFFFFFFFF) + hash(slot) & 0xFFFFFFFF
                continue
            for value in slot:
                hv = (37 * hv & 0xFFFFFFFF) + hash(value) & 0xFFFFFFFF
        extra = list(self.__extra__.items())
        extra.sort(key=lambda kv: kv[0])
        for uri, value in extra:
            hv = (37 * hv & 0xFFFFFFFF) + hash(uri) & 0xFFFFFFFF
            hv = (37 * hv & 0xFFFFFFFF) + hash(value) & 0xFFFFFFFF
        return hv

    async def __jsonld__(
        self, *, expand: bool = False, loader: Optional[DocumentLoader] = None
    ) -> Mapping[str, Any]:
        doc: dict[str, Any] = {"@type": type(self).__uri__}
        for uri, slot in self._values.items():
            if isinstance(slot, str):
                doc[uri] = slot
                continue
            doc[uri] = [
                (
                    {"@id": v}
                    if isinstance(v, EntityRef)
                    else await to_jsonld(v, expand=True, loader=loader)
                )
                for v in slot
            ]
        for uri, value in self.__extra__.items():
            doc[uri] = value
        doc_loader = get_raw_document_loader(loader)
        if expand:
            return await to_thread(
                lambda: jsonld.expand(
                    doc,
                    {"documentLoader": doc_loader},
                )[0]
            )
        return await to_thread(
            lambda: jsonld.compact(
                doc,
                type(self).__default_context__,
                {"documentLoader": doc_loader},
            )
        )

    def __repr__(self) -> str:
        cls = type(self)
        uri_props = get_uri_descriptors(cls)
        value_map = {}
        for uri, values in self._values.items():
            props = uri_props.get(uri, {})
            for name, descriptor in props.items():
                if descriptor.check_slot(values):
                    value_map[name] = descriptor.repr_value(values)
                    break
        if self.__extra__:
            value_map["__extra__"] = self.__extra__
        args = ", ".join(f"{k}={v!r}" for (k, v) in value_map.items())
        return f"{cls.__name__}({args})"


entity_types: dict[Uri, type[Entity]] = {}


def get_entity_type(type_uri: Uri) -> Optional[type[Entity]]:
    if not entity_types:

        def collect_entity_types(cls: type[Entity]) -> None:
            global entity_types
            for subclass in cls.__subclasses__():
                if subclass.__uri__ not in entity_types:
                    entity_types[subclass.__uri__] = subclass
            for subclass in cls.__subclasses__():
                collect_entity_types(subclass)

        collect_entity_types(Entity)
    return entity_types.get(type_uri)


descriptors: dict[type[Entity], Mapping[str, Property]] = {}


def get_descriptors(cls: type[Entity]) -> Mapping[str, Property]:
    global descriptors
    properties = descriptors.get(cls)
    if properties is None:
        properties = {
            name: getattr(cls, name)
            for name in dir(cls)
            if isinstance(getattr(cls, name), Property)
        }
        descriptors[cls] = properties
    return properties


uri_descriptors: dict[type[Entity], Mapping[Uri, Mapping[str, Property]]] = {}


def get_uri_descriptors(
    cls: type[Entity],
) -> Mapping[Uri, Mapping[str, Property]]:
    global uri_descriptors
    if cls in uri_descriptors:
        return uri_descriptors[cls]
    uri_props: dict[Uri, dict[str, Property]] = {}
    props = get_descriptors(cls)
    for name, prop in props.items():
        uri_props.setdefault(prop.uri, {})[name] = prop
    uri_descriptors[cls] = uri_props
    return uri_props


def get_raw_document_loader(loader: Optional[DocumentLoader] = None) -> Any:
    if loader is None:
        orig_loader = requests_document_loader()
        return lambda url, options: orig_loader(
            url,
            {
                **options,
                "headers": {
                    **options.get("headers", {}),
                    "Accept": "application/ld+json, application/json",
                },
            },
        )

    def doc_loader(url: str, options: Any) -> Any:
        document = loader(url)
        if document is None:
            raise jsonld.JsonLdError(
                f"failed to load remote document: {url!r}",
                "jsonld.LoadDocumentError",
                code="loading document failed",
            )
        return {
            "contentType": document.content_type,
            "contextUrl": document.context_url,
            "documentUrl": document.url,
            "document": document.document,
        }

    return doc_loader


T = TypeVar("T", bound=Entity)


class EntityRef:
    """A reference to an :class:`Entity`.  It is used to represent references
    to entities in other entities, which are not loaded yet.
    """

    #: The URI of the entity.
    uri: Uri

    def __init__(self, uri: Uri | str) -> None:
        self.uri = cast(Uri, uri)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, EntityRef) and self.uri == other.uri

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash(self.uri)

    async def load(
        self, cls: type[T], loader: Optional[DocumentLoader] = None
    ) -> T:
        """Resolve the reference and load the entity.

        :param cls: The class to load the entity as.  It must be a subclass of
            :class:`Entity`.
        :param loader: A document loader to use.  If not given, the default
            document loader will be used.
        :return: The loaded entity.
        """
        if not issubclass(cls, Entity):
            raise TypeError(f"expected a subtype of Entity, got {cls!r}")
        document_loader = get_raw_document_loader(loader)
        loaded = await to_thread(lambda: document_loader(self.uri, {}))
        doc = await to_thread(
            lambda: jsonld.expand(
                loaded["document"],
                {
                    "documentLoader": document_loader,
                    "expandContext": loaded["contextUrl"],
                },
            )
        )
        return await cls.__from_jsonld__(doc[0], loader=loader)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.uri!r})"


async def load_entity_refs(
    entity: Entity,
    properties: Optional[str | Iterable[str]] = None,
    loader: Optional[DocumentLoader] = None,
) -> None:
    r"""Resolve :class:`EntityRef`\ s and replace them with the loaded
    :class:`Entity` instances in the given :paramref:`entity`.

    :param entity: The entity to resolve references in.
    :param properties: The properties to resolve references in.  If not given,
        all properties will be resolved.
    :param loader: A document loader to use.  If not given, the default
        document loader will be used.
    """
    descriptors = get_descriptors(type(entity))
    if properties is not None:
        if isinstance(properties, str):
            properties = [properties]
        for prop in properties:
            if prop not in descriptors:
                raise AttributeError(
                    f"{type(entity).__name__} has no property named {prop!r}"
                )
    for name, descriptor in descriptors.items():
        if properties is not None and name not in properties:
            continue
        slot = entity._values.get(descriptor.uri)
        if slot is None or isinstance(slot, str):
            continue
        for i, value in enumerate(slot):
            if isinstance(value, EntityRef):
                slot[i] = await value.load(Entity, loader=loader)
