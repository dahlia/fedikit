from typing import Generic, NamedTuple, Optional, Sequence, TypeVar

__all__ = ["Page"]


TItem = TypeVar("TItem")


class Page(NamedTuple, Generic[TItem]):
    """A page of items."""

    prev_cursor: Optional[str]
    next_cursor: Optional[str]
    items: Sequence[TItem]
