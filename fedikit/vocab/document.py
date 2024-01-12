from ..uri import Uri
from .object import Object

__all__ = ["Audio", "Document", "Image", "Page", "Video"]


class Document(Object):
    """Represents a document of any kind."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Document")
    __default_context__ = Uri("https://www.w3.org/ns/activitystreams")


class Audio(Document):
    """Represents an audio document of any kind."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Audio")


class Image(Document):
    """An image document of any kind."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Image")


class Page(Document):
    """Represents a web page."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Page")


class Video(Document):
    """Represents a video document of any kind."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Video")
