import typing
from abc import ABC, abstractmethod, abstractproperty
from collections.abc import Sequence
from importlib import import_module
from inspect import currentframe
from types import GenericAlias, UnionType
from typing import Any, ForwardRef, NewType, Optional, Self, Union

from ..uri import Uri
from .converters import from_jsonld
from .docloader import DocumentLoader

if typing.TYPE_CHECKING:
    from .entity import Entity, EntityRef, Slot
    from .scalars import ScalarValue

__all__ = [
    "IdProperty",
    "PluralProperty",
    "Property",
    "ResourceProperty",
    "SingularProperty",
    "id_property",
    "plural_property",
    "singular_property",
]


class Property(ABC):
    @abstractproperty
    def uri(self) -> "Uri":
        raise NotImplementedError

    @abstractmethod
    def __get__(
        self, instance: Any | None, cls: type["Entity"]
    ) -> Self | Any | Sequence[Any]: ...

    @abstractmethod
    def normalize(self, value: Any) -> "Slot": ...

    @abstractmethod
    def check_slot(self, slot: "Slot") -> bool: ...

    def repr_value(self, slot: "Slot") -> Any:
        return slot

    @abstractmethod
    async def parse_jsonld(
        self, type_: Any, value: Any, loader: Optional[DocumentLoader] = None
    ) -> Union[
        "Uri",
        "EntityRef",
        "ScalarValue",
        "Entity",
        Sequence[Union["EntityRef", "ScalarValue", "Entity"]],
    ]: ...


class IdProperty(Property):
    @property
    def uri(self) -> "Uri":
        return Uri("@id")

    def __get__(
        self, instance: Any | None, cls: type["Entity"]
    ) -> Self | "Uri":
        if instance is None:
            return self
        return instance._values["@id"]  # type: ignore

    def normalize(self, value: Any) -> "Slot":
        assert isinstance(value, str)
        return Uri(value)

    def check_slot(self, slot: "Slot") -> bool:
        return isinstance(slot, str)

    async def parse_jsonld(
        self, type_: Any, value: Any, loader: Optional[DocumentLoader] = None
    ) -> Union[
        "Uri",
        "EntityRef",
        "ScalarValue",
        "Entity",
        Sequence[Union["EntityRef", "ScalarValue", "Entity"]],
    ]:
        if type_ is not Uri:
            raise TypeError(f"expected Uri, got {type_.__name__}")
        return Uri(value)


class ResourceProperty(Property):
    subproperties: Sequence["Uri"]
    class_def_site: Optional[str]
    _uri: "Uri"

    def __init__(self, uri: "Uri", subproperties: Sequence["Uri"] = ()):
        self._uri = uri
        self.subproperties = subproperties
        current_frame = currentframe()
        if current_frame is None:
            self.class_def_site = None
        else:
            current_filename = current_frame.f_code.co_filename
            while (
                current_frame is not None
                and current_frame.f_code.co_filename == current_filename
            ):
                current_frame = current_frame.f_back
            self.class_def_site = (
                current_frame and current_frame.f_globals.get("__name__")
            )

    @property
    def uri(self) -> "Uri":
        return self._uri


class PluralProperty(ResourceProperty):
    def __get__(
        self, instance: Any | None, cls: type["Entity"]
    ) -> Self | Sequence[Any]:
        if instance is None:
            return self
        from .entity import EntityRef

        values = []
        for uri in (self.uri, *self.subproperties):
            for v in instance._values[uri]:
                if isinstance(v, EntityRef):
                    continue
                values.append(v)
        return values

    def normalize(self, value: Any) -> "Slot":
        return [v for v in value]

    def check_slot(self, slot: "Slot") -> bool:
        return not isinstance(slot, str) and len(slot) != 1

    async def parse_jsonld(
        self, type_: Any, value: Any, loader: Optional[DocumentLoader] = None
    ) -> Union[
        "Uri",
        "EntityRef",
        "ScalarValue",
        "Entity",
        Sequence[Union["EntityRef", "ScalarValue", "Entity"]],
    ]:
        if not (
            isinstance(
                type_,
                (GenericAlias, typing._GenericAlias),  # type: ignore
            )
            and type_.__origin__ in (Sequence, typing.Sequence)
        ):
            raise TypeError(f"expected Sequence[T], got {type_!r}")
        element_type = type_.__args__[0]
        if isinstance(element_type, UnionType):
            element_types = list(element_type.__args__)
        elif (
            isinstance(element_type, typing._GenericAlias)  # type: ignore
            and element_type.__origin__ is Union
        ):
            element_types = list(element_type.__args__)
        elif isinstance(element_type, NewType):
            element_types = [element_type.__supertype__]
        else:
            element_types = [element_type]
        for i, et in enumerate(element_types):
            if isinstance(et, (str, ForwardRef)):
                et_name = et if isinstance(et, str) else et.__forward_arg__
                et = self.class_def_site and getattr(
                    import_module(self.class_def_site), et_name, None
                )
                if et is None or not isinstance(et, type):
                    raise ReferenceError(
                        f"failed to resolve deferred type name {et_name!r}"
                    )
                element_types[i] = et
            elif et is Uri:
                element_types[i] = str
            elif isinstance(et, typing._LiteralGenericAlias):  # type: ignore
                element_types[i] = str  # FIXME: support other literal types
        if not all(isinstance(et, type) for et in element_types):
            raise TypeError(
                f"expected Sequence[T] where T is a class, got {type_!r}"
            )
        parsed = []
        for v in value:
            if len(v) == 1 and "@id" in v:
                from .entity import EntityRef

                parsed.append(EntityRef(v["@id"]))
                continue
            for et in element_types:
                try:
                    parsed.append(
                        await from_jsonld(
                            et, v, loader=loader  # pyright: ignore
                        )
                    )
                except ValueError:
                    continue
                else:
                    break
        return parsed


class SingularProperty(ResourceProperty):
    def __get__(self, instance: Any | None, cls: type["Entity"]) -> Self | Any:
        if instance is None:
            return self
        from .entity import EntityRef

        for uri in (self.uri, *self.subproperties):
            for v in instance._values[uri]:
                if not isinstance(v, EntityRef):
                    return v
        return None

    def normalize(self, value: Any) -> "Slot":
        return [(value)]

    def check_slot(self, slot: "Slot") -> bool:
        return not isinstance(slot, str) and len(slot) == 1

    def repr_value(self, slot: "Slot") -> Any:
        return slot[0]

    async def parse_jsonld(
        self, type_: Any, value: Any, loader: Optional[DocumentLoader] = None
    ) -> Union[
        "Uri",
        "EntityRef",
        "ScalarValue",
        "Entity",
        Sequence[Union["EntityRef", "ScalarValue", "Entity"]],
    ]:
        if isinstance(type_, UnionType):
            types = list(type_.__args__)
        elif (
            isinstance(type_, typing._GenericAlias)  # type: ignore
            and type_.__origin__ is Union
        ):
            types = list(type_.__args__)
        elif isinstance(type_, NewType):
            types = [type_.__supertype__]
        else:
            types = [type_]
        for i, t in enumerate(types):
            if isinstance(t, (str, ForwardRef)):
                t_name = t if isinstance(t, str) else t.__forward_arg__
                t = self.class_def_site and getattr(
                    import_module(self.class_def_site), t_name, None
                )
                if t is None or not isinstance(t, type):
                    raise ReferenceError(
                        f"failed to resolve deferred type name {t_name!r}"
                    )
                types[i] = t
            elif t is Uri:
                types[i] = str
            elif isinstance(t, typing._LiteralGenericAlias):  # type: ignore
                types[i] = str  # FIXME: support other literal types
        if not all(isinstance(t, type) for t in types):
            raise TypeError(
                "expected T or Union[T, ...] where T is a class, got"
                f" {type_!r}"
            )
        for v in value:
            if len(v) == 1 and "@id" in v:
                from .entity import EntityRef

                return EntityRef(v["@id"])
            for t in types:
                try:
                    return await from_jsonld(
                        t, v, loader=loader  # pyright: ignore
                    )
                except ValueError:
                    continue
        raise ValueError(f"cannot convert {value!r} to {type_.__name__}")


def id_property() -> Any:
    return IdProperty()


def plural_property(uri: "Uri", subproperties: Sequence["Uri"] = ()) -> Any:
    return PluralProperty(uri, subproperties=subproperties)


def singular_property(uri: "Uri", subproperties: Sequence["Uri"] = ()) -> Any:
    return SingularProperty(uri, subproperties=subproperties)
