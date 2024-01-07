from collections.abc import Sequence
from datetime import datetime
from typing import Union

from isoduration.types import Duration

from ..model.descriptors import id_property, plural_property, singular_property
from ..model.entity import Entity, Uri
from ..model.langstr import LanguageString
from .link import Link

__all__ = ["Object"]


class Object(Entity):
    """Describes an object of any kind.  The ``Object`` type serves as the base
    type for most of the other kinds of objects defined in the Activity
    Vocabulary, including other Core types such as :class:`Activity`,
    :class:`IntransitiveActivity`, :class:`Collection` and
    :class:`OrderedCollection`.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Object")
    __default_context__ = Uri("https://www.w3.org/ns/activitystreams")

    #: Provides the globally unique identifier for an :class:`Object`.
    id: Uri = id_property()

    #: Identifies a resource attached or related to an object that potentially
    #: requires special handling.  The intent is to provide a model that is
    #: at least semantically similar to attachments in email.
    attachment: Union["Object", Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#attachment")
    )

    #: Plural accessor for :attr:`attachment`.
    attachments: Sequence[Union["Object", Link]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#attachment")
    )

    #: Identifies one or more entities to which this object is attributed.
    #: The attributed entities might not be :class:`Actor`\ s.  For instance,
    #: an object might be attributed to the completion of another activity.
    attributed_to: Union["Object", Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#attributedTo")
    )

    #: Plural accessor for :attr:`attributed_to`.
    attributed_tos: Sequence[Union["Object", Link]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#attributedTo")
    )

    #: Identifies one or more entities that represent the total population of
    #: entities for which the object can considered to be relevant.
    audience: Union["Object", Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#audience")
    )

    #: Plural accessor for :attr:`audience`.
    audiences: Sequence[Union["Object", Link]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#audience")
    )

    #: The content or textual representation of the ``Object`` encoded as
    #: a JSON string.  By default, the value of content is HTML.
    #: The :attr:`mediaType` property can be used in the object to indicate
    #: a different content type.
    #:
    #: The content *may* be expressed using multiple language-tagged values.
    content: str | LanguageString = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#content")
    )

    #: Plural accessor for :attr:`content`.
    contents: Sequence[str | LanguageString] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#content")
    )

    #: Identifies the context within which the object exists or an activity
    #: was performed.
    #:
    #: The notion of "context" used is intentionally vague.  The intended
    #: function is to serve as a means of grouping objects and activities that
    #: share a common originating context or purpose. An example could be
    #: all activities relating to a common project or event.
    context: Union["Object", Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#context")
    )

    #: Plural accessor for :attr:`context`.
    contexts: Sequence[Union["Object", Link]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#context")
    )

    #: A simple, human-readable, plain-text name for the object.
    #: HTML markup *must not* be included.
    #: The name *may* be expressed using multiple language-tagged values.
    name: str | LanguageString = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#name")
    )

    #: Plural accessor for :attr:`name`.
    names: Sequence[str | LanguageString] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#name")
    )

    #: The date and time describing the actual or expected ending time of
    #: the object.  When used with an :class:`Activity` object, for instance,
    #: the :attr:`end_time` property specifies the moment the activity
    #: concluded or is expected to conclude.
    end_time: datetime = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#endTime")
    )

    #: Identifies the entity (e.g. an application) that generated the object.
    generator: Union["Object", Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#generator")
    )

    #: Plural accessor for :attr:`generator`.
    generators: Sequence[Union["Object", Link]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#generator")
    )

    #: Indicates an entity that describes an icon for this object.
    #: The image should have an aspect ratio of one (horizontal) to
    #: one (vertical) and should be suitable for presentation at a small size.
    icon: Union["Image", Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#icon")
    )

    #: Plural accessor for :attr:`icon`.
    icons: Sequence[Union["Image", Link]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#icon")
    )

    #: Indicates an entity that describes an image for this object.
    #: Unlike the :attr:`icon` property, there are no aspect ratio or display
    #: size limitations assumed.
    image: Union["Image", Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#image")
    )

    #: Plural accessor for :attr:`image`.
    images: Sequence[Union["Image", Link]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#image")
    )

    #: Indicates one or more entities for which this object is considered
    #: a response.
    in_reply_to: Union["Object", Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#inReplyTo")
    )

    #: Plural accessor for :attr:`in_reply_to`.
    in_reply_tos: Sequence[Union["Object", Link]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#inReplyTo")
    )

    #: Indicates one or more physical or logical locations associated with
    #: the object.
    location: Union["Object", Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#location")
    )

    #: Plural accessor for :attr:`location`.
    locations: Sequence[Union["Object", Link]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#location")
    )

    #: Identifies an entity that provides a preview of this object.
    preview: Union["Link", "Object"] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#preview")
    )

    #: Plural accessor for :attr:`preview`.
    previews: Sequence[Union["Link", "Object"]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#preview")
    )

    #: The date and time at which the object was published.
    published: datetime = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#published")
    )

    #: Identifies a :class:`Collection` containing objects considered to be
    #: responses to this object.
    replies: "Collection" = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#replies")
    )

    #: The date and time describing the actual or expected starting time of
    #: the object.  When used with an :class:`Activity` object, for instance,
    #: the :attr:`start_time` property specifies the moment the activity
    #: began or is scheduled to begin.
    start_time: datetime = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#startTime")
    )

    #: A natural language summarization of the object encoded as HTML.
    #: Multiple language tagged summaries *may* be provided.
    summary: str | LanguageString = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#summary")
    )

    #: Plural accessor for :attr:`summary`.
    summaries: Sequence[str | LanguageString] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#summary")
    )

    #: One or more "tags" that have been associated with an objects.
    #: A tag can be any kind of :class:`Object`.  The key difference between
    #: :attr:`attachment` and :attr:`tag` is that the former implies
    #: association by inclusion, while the latter implies associated
    #: by reference.
    tag: Union["Link", "Object"] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#tag")
    )

    #: Plural accessor for :attr:`tag`.
    tags: Sequence[Union["Link", "Object"]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#tag")
    )

    #: The date and time at which the object was updated.
    updated: datetime = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#updated")
    )

    #: Identifies one or more links to representations of the object.
    url: Uri | Link = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#url")
    )

    #: Plural accessor for :attr:`url`.
    urls: Sequence[Uri | Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#url")
    )

    #: Identifies an entity considered to be part of the public primary
    #: audience of an :class:`Object`.
    to: Union["Link", "Object"] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#to")
    )

    #: Plural accessor for :attr:`to`.
    tos: Sequence[Union["Link", "Object"]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#to")
    )

    #: Identifies an entity considered to be part of the public primary
    #: audience of an :class:`Object`.
    bto: Union["Link", "Object"] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#bto")
    )

    #: Plural accessor for :attr:`bto`.
    btos: Sequence[Union["Link", "Object"]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#bto")
    )

    #: Identifies an :class:`Object` that is part of the public secondary
    #: audience of this :class:`Object`.
    cc: Union["Link", "Object"] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#cc")
    )

    #: Plural accessor for :attr:`cc`.
    ccs: Sequence[Union["Link", "Object"]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#cc")
    )

    #: Singular accessor for :attr:`bccs`.
    bcc: Union["Link", "Object"] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#bcc")
    )

    #: Identifies one or more :class:`Object`\ s that are part of the private
    #: secondary audience of this :class:`Object`.
    bccs: Sequence[Union["Link", "Object"]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#bcc")
    )

    #: Identifies the MIME media type of the value of the :attr:`content`
    #: property.  If not specified, the :attr:`content` property is assumed to
    #: contain ``text/html`` content.
    mediaType: str = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#mediaType")
    )

    #: When the object describes a time-bound resource, such as an audio or
    #: video, a meeting, etc, the :attr:`duration` property indicates
    #: the object's approximate duration.  The value *must* be expressed as
    #: an ``xsd:duration`` as defined by `W3C XML Schema Definition Language
    #: (XSD) 1.1 Part 2: Datatypes`__, section 3.3.6 (e.g. a period of
    #: 5 seconds is represented as "PT5S").
    #:
    #: __ https://www.w3.org/TR/xmlschema11-2/
    duration: Duration = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#duration")
    )


from .collection import Collection  # noqa: E402
from .document import Image  # noqa: E402
