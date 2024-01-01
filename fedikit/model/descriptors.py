import typing
from abc import ABC, abstractmethod, abstractproperty
from collections.abc import Sequence
from types import GenericAlias, UnionType
from typing import Any, Self

from .converters import from_jsonld

if typing.TYPE_CHECKING:
    from .entity import Entity, Slot, Uri

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
    ) -> Self | Any | Sequence[Any]:
        raise NotImplementedError

    @abstractmethod
    def normalize(self, value: Any) -> "Slot":
        raise NotImplementedError

    @abstractmethod
    def check_slot(self, slot: "Slot") -> bool:
        raise NotImplementedError

    @abstractmethod
    async def parse_jsonld(self, type_: Any, value: Any) -> Any:
        raise NotImplementedError


class IdProperty(Property):
    @property
    def uri(self) -> "Uri":
        from .entity import Uri

        return Uri("@id")

    def __get__(
        self, instance: Any | None, cls: type["Entity"]
    ) -> Self | "Uri":
        if instance is None:
            return self
        return instance._values["@id"]  # type: ignore

    def normalize(self, value: Any) -> "Slot":
        from .entity import Uri

        assert isinstance(value, str)
        return Uri(value)

    def check_slot(self, slot: "Slot") -> bool:
        return isinstance(slot, str)

    async def parse_jsonld(self, type_: Any, value: Any) -> Any:
        if type_ is not Uri:
            raise TypeError(f"expected Uri, got {type_.__name__}")
        return Uri(value)


class ResourceProperty(Property):
    _uri: "Uri"

    def __init__(self, uri: "Uri"):
        self._uri = uri

    @property
    def uri(self) -> "Uri":
        return self._uri


class PluralProperty(ResourceProperty):
    def __get__(
        self, instance: Any | None, cls: type["Entity"]
    ) -> Self | Sequence[Any]:
        if instance is None:
            return self
        values = []
        for slot_type, value in instance._values[self.uri]:
            assert (
                slot_type == "resource"
            ), f"expected 'resource', got {slot_type!r}"
            values.append(value)
        return values

    def normalize(self, value: Any) -> "Slot":
        return [("resource", v) for v in value]

    def check_slot(self, slot: "Slot") -> bool:
        return not isinstance(slot, str) and len(slot) != 1

    async def parse_jsonld(self, type_: Any, value: Any) -> Any:
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
            element_types = element_type.__args__
        elif (
            isinstance(element_type, typing._GenericAlias)  # type: ignore
            and element_type.__origin__ is UnionType
        ):
            element_types = element_type.__args__
        elif isinstance(element_type, type):
            element_types = (element_type,)
        else:
            raise TypeError(
                f"expected Sequence[T] where T is a class, got {type_!r}"
            )
        parsed = []
        for v in value:
            for et in element_types:
                try:
                    parsed.append(await from_jsonld(et, v))
                except ValueError:
                    continue
                else:
                    break
        return parsed


class SingularProperty(ResourceProperty):
    def __get__(self, instance: Any | None, cls: type["Entity"]) -> Self | Any:
        if instance is None:
            return self
        values = instance._values[self.uri]
        if values:
            slot = values[0]
            assert (
                slot[0] == "resource"
            ), f"expected 'resource', got {slot[0]!r}"
            return slot[1]
        return None

    def normalize(self, value: Any) -> "Slot":
        return [("resource", value)]

    def check_slot(self, slot: "Slot") -> bool:
        return not isinstance(slot, str) and len(slot) == 1

    async def parse_jsonld(self, type_: Any, value: Any) -> Any:
        if isinstance(type_, UnionType):
            types = type_.__args__
        elif (
            isinstance(type_, typing._GenericAlias)  # type: ignore
            and type_.__origin__ is UnionType
        ):
            types = type_.__args__
        elif isinstance(type_, type):
            types = (type_,)
        else:
            raise TypeError(
                "expected T or Union[T, ...] where T is a class, got"
                f" {type_!r}"
            )
        for v in value:
            for et in types:
                try:
                    return await from_jsonld(et, v)
                except ValueError:
                    continue
        raise ValueError(f"cannot convert {value!r} to {type_.__name__}")


def id_property() -> Any:
    return IdProperty()


def plural_property(uri: "Uri") -> Any:
    return PluralProperty(uri)


def singular_property(uri: "Uri") -> Any:
    return SingularProperty(uri)
