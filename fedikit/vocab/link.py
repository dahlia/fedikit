from collections.abc import Sequence

from ..model.descriptors import id_property, plural_property, singular_property
from ..model.entity import Entity, Uri
from ..model.langstr import LanguageString

__all__ = ["Link"]


class Link(Entity):
    """A Link is an indirect, qualified reference to a resource identified by
    a URL.  The fundamental model for links is established by :rfc:`5988`.
    Many of the properties defined by the Activity Vocabulary allow values that
    are either instances of :class:`Object` or ``Link``.  When a ``Link`` is
    used, it establishes a `qualified relation`__ connecting the subject
    (the containing object) to the resource identified by the :attr:`href`.
    Properties of the ``Link`` are properties of the reference as opposed to
    properties of the resource.

    __ http://patterns.dataincubator.org/book/qualified-relation.html
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Link")
    __default_context__ = Uri("https://www.w3.org/ns/activitystreams")

    #: Provides the globally unique identifier for an :class:`Link`.
    id: Uri = id_property()

    #: The target resource pointed to by a :class:`Link`.
    href: Uri = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#href")
    )

    #: A simple, human-readable, plain-text name for the object.
    #: HTML markup *must not* be included.
    #: The name *may* be expressed using multiple language-tagged values.
    name: str | LanguageString = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#name")
    )

    #: Simple, human-readable, plain-text names for the object.
    #: HTML markup *must not* be included.
    #: The names *may* be expressed using multiple language-tagged values.
    names: Sequence[str | LanguageString] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#name")
    )
