from collections.abc import Sequence
from typing import Optional, Union

from langcodes import Language

from ..model.descriptors import id_property, plural_property, singular_property
from ..model.entity import Entity
from ..model.langstr import LanguageString
from ..uri import Uri

__all__ = ["Link", "Mention"]


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

    __abstract__ = False
    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Link")
    __default_context__ = Uri("https://www.w3.org/ns/activitystreams")

    #: Provides the globally unique identifier for an :class:`Link`.
    id: Uri = id_property()

    #: The target resource pointed to by a :class:`Link`.
    href: Optional[Uri] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#href")
    )

    #: A link relation associated with a :class:`Link`. The value *must*
    #: conform to both the HTML5_ and :rfc:`5988` "link relation" definitions.
    #:
    #: In the HTML5_, any string not containing the "space" U+0020, "tab"
    #: (U+0009), "LF" (U+000A), "FF" (U+000C), "CR" (U+000D) or "," (U+002C)
    #: characters can be used as a valid link relation.
    #:
    #: .. _HTML5: https://www.w3.org/TR/html5/
    rel: Optional[str] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#rel")
    )

    #: Plural accessor for :attr:`rel`.
    rels: Sequence[str] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#rel")
    )

    #: Identifies the MIME media type of the referenced resource.
    media_type: Optional[str] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#mediaType")
    )

    #: A simple, human-readable, plain-text name for the object.
    #: HTML markup *must not* be included.
    #: The name *may* be expressed using multiple language-tagged values.
    name: Optional[str | LanguageString] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#name")
    )

    #: Plural accessor for :attr:`name`.
    names: Sequence[str | LanguageString] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#name")
    )

    #: Hints as to the language used by the target resource.  Value *must* be a
    #: BCP47_ Language-Tag.
    #:
    #: .. _BCP47: https://tools.ietf.org/html/bcp47
    hreflang: Optional[Language] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#hreflang")
    )

    #: On a :class:`Link`, specifies a hint as to the rendering height in
    #: device-independent pixels of the linked resource.
    height: Optional[int] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#height")
    )

    #: On a :class:`Link`, specifies a hint as to the rendering width in
    #: device-independent pixels of the linked resource.
    width: Optional[int] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#width")
    )

    #: Identifies an entity that provides a preview of this object.
    preview: Optional[Union["Link", "Object"]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#preview")
    )

    #: Plural accessor for :attr:`preview`.
    previews: Sequence[Union["Link", "Object"]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#preview")
    )


class Mention(Link):
    """A specialized :class:`Link` that represents an @mention."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Mention")


from .object import Object  # noqa: E402
