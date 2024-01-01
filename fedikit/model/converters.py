from datetime import datetime
from typing import Any, Mapping, Optional, TypeVar

from .docloader import DocumentLoader

__all__ = ["from_jsonld", "jsonld"]


async def jsonld(
    value: Any, expand: bool = False, loader: Optional[DocumentLoader] = None
) -> Mapping[str, Any]:
    """Turn a Python object into a JSON-LD document.

    :param value: A Python object to convert.
    :param expand: Whether to expand the document.  Compact it otherwise.
    :param loader: A document loader to use.  If not given, the default
        document loader will be used.
    :return: The JSON-LD document.
    :raises TypeError: If the given value cannot be converted to JSON-LD.
    """
    if hasattr(value, "__jsonld__"):
        doc = value.__jsonld__(expand=expand, loader=loader)
        return dict(doc if isinstance(doc, Mapping) else await doc)
    match value:
        case str() | bool():
            return {"@value": value}
        case int():
            return {
                "@value": value,
                "@type": (
                    "http://www.w3.org/2001/XMLSchema#integer"
                    if value < 0
                    else "http://www.w3.org/2001/XMLSchema#nonNegativeInteger"
                ),
            }
        case datetime():
            return {
                "@type": "http://www.w3.org/2001/XMLSchema#dateTime",
                "@value": value.isoformat(),
            }
    raise TypeError(f"cannot convert {type(value).__name__} to JSON-LD")


T = TypeVar("T")


async def from_jsonld(cls: type[T], document: Mapping[str, Any]) -> T:
    """Turn a JSON-LD document into a Python object.

    :param cls: The class to convert the document to.
    :param document: The JSON-LD document to convert.
    :return: The converted object.
    :raises ValueError: If the given document cannot be converted to the
        given class.
    """
    if hasattr(cls, "__from_jsonld__"):
        instance = cls.__from_jsonld__(document)  # type: ignore
        return (  # type: ignore
            instance if isinstance(instance, cls) else await instance
        )
    elif issubclass(cls, (str, bool)):
        return cls(document["@value"])  # type: ignore
    elif issubclass(cls, int):
        return cls(document["@value"])  # type: ignore
    elif issubclass(cls, datetime):
        return cls.fromisoformat(document["@value"])  # type: ignore
    raise ValueError(f"cannot convert JSON-LD to {cls.__name__}")
