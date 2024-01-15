from dataclasses import dataclass
from datetime import datetime

__all__ = ["Metadata", "MetadataWithCreated", "Post"]


@dataclass(frozen=True)
class Metadata:
    handle: str
    title: str
    description: str


@dataclass(frozen=True)
class MetadataWithCreated(Metadata):
    created: datetime


@dataclass(frozen=True)
class Post:
    id: int
    content: str
    published: datetime
