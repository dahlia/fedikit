from asyncio import to_thread
from collections.abc import Mapping, Sequence
from typing import (
    Any,
    ClassVar,
    Literal,
    NewType,
    Optional,
    Self,
    TypeAlias,
    dataclass_transform,
)

from pyld import jsonld
from pyld.documentloader.requests import requests_document_loader

from .converters import jsonld as to_jsonld
from .descriptors import Property
from .docloader import DocumentLoader

__all__ = ["Entity", "Slot", "Uri"]


Uri = NewType("Uri", str)


Slot: TypeAlias = (
    Uri | Sequence[tuple[Literal["id"], Uri] | tuple[Literal["resource"], Any]]
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
        if "@type" not in doc:
            raise ValueError("missing '@type' in JSON-LD document")
        elif cls.__uri__ not in doc["@type"]:
            for subclass in cls.__subclasses__():
                if subclass.__uri__ in doc["@type"]:
                    assert issubclass(subclass, cls)
                    return await subclass.__from_jsonld__(doc)
            raise ValueError(
                f"expected type {cls.__uri__!r}, got {doc['@type']!r}"
            )
        values: dict[str, Any] = {}
        extra: dict[Uri, Any] = {}
        descriptors: Mapping[Uri, Mapping[str, Property]] = (
            get_uri_descriptors(cls)
        )
        for uri, vals in doc.items():
            desc_dict = descriptors.get(Uri(uri), {})
            for name, desc in desc_dict.items():
                try:
                    values[name] = await desc.parse_jsonld(
                        cls.__annotations__[name], vals
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
            for slot_type, value in slot:
                hv = (37 * hv & 0xFFFFFFFF) + hash(slot_type) & 0xFFFFFFFF
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
                await to_jsonld(v, expand=True, loader=loader) for _, v in slot
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
            for name, prop in props.items():
                if prop.check_slot(values):
                    value_map[name] = getattr(self, name)
                    break
        if self.__extra__:
            value_map["__extra__"] = self.__extra__
        args = ", ".join(f"{k}={v!r}" for (k, v) in value_map.items())
        return f"{cls.__name__}({args})"


def get_descriptors(cls: type) -> Mapping[str, Property]:
    if hasattr(cls, "__descriptors__"):
        return cls.__descriptors__  # type: ignore
    properties = {
        name: getattr(cls, name)
        for name in dir(cls)
        if isinstance(getattr(cls, name), Property)
    }
    cls.__descriptors__ = properties  # type: ignore
    return properties


def get_uri_descriptors(
    cls: type,
) -> Mapping[Uri, Mapping[str, Property]]:
    if hasattr(cls, "__uri_descriptors__"):
        return cls.__uri_descriptors__  # type: ignore
    uri_props: dict[Uri, dict[str, Property]] = {}
    props = get_descriptors(cls)
    for name, prop in props.items():
        uri_props.setdefault(prop.uri, {})[name] = prop
    cls.__uri_descriptors__ = uri_props  # type: ignore
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
