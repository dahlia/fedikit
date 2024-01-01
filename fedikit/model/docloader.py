from collections.abc import Mapping
from dataclasses import dataclass
from typing import Callable, Optional, Sequence, TypeAlias

__all__ = ["DocumentLoader", "Json", "RemoteDocument"]


#: A type alias for JSON values.
Json: TypeAlias = (
    Mapping[str, "Json"] | Sequence["Json"] | str | int | float | bool | None
)


@dataclass(frozen=True)
class RemoteDocument:
    """A remote JSON-LD document loaded from a URL."""

    #: The document's media type, e.g. ``application/ld+json``.
    content_type: str

    #: An optional URL for the document's context, which is referred by
    #: a ``Link`` header in the document.
    context_url: Optional[str]

    #: The URL from which the document was loaded.  This may differ from
    #: the URL passed to the document loader if the document was
    #: redirected.
    url: str

    #: The document's JSON content.
    document: Json


#: A document loader which is a function that takes a URL and returns
#: a :class:`Document`.
DocumentLoader: TypeAlias = Callable[[str], Optional[RemoteDocument]]
