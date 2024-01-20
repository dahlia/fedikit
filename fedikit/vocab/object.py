from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, ClassVar, Literal, Optional, Union

from isoduration.types import Duration

from ..model.descriptors import id_property, plural_property, singular_property
from ..model.entity import Entity, EntityRef
from ..model.langstr import LanguageString
from ..uri import Uri
from .link import Link

__all__ = [
    "Article",
    "Event",
    "Note",
    "Object",
    "Place",
    "Profile",
    "Relationship",
    "Tombstone",
]


class Object(Entity):
    """Describes an object of any kind.  The ``Object`` type serves as the base
    type for most of the other kinds of objects defined in the Activity
    Vocabulary, including other Core types such as :class:`Activity`,
    :class:`IntransitiveActivity`, :class:`Collection` and
    :class:`OrderedCollection`.
    """

    __abstract__ = False
    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Object")
    __default_context__: ClassVar[Uri | Sequence[Uri] | Mapping[str, Any]] = (
        Uri("https://www.w3.org/ns/activitystreams")
    )

    #: Provides the globally unique identifier for an :class:`Object`.
    id: Uri = id_property()

    #: Identifies a resource attached or related to an object that potentially
    #: requires special handling.  The intent is to provide a model that is
    #: at least semantically similar to attachments in email.
    attachment: Optional[Union[EntityRef, "Object", Link]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#attachment")
    )

    #: Plural accessor for :attr:`attachment`.
    attachments: Sequence[Union[EntityRef, "Object", Link]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#attachment")
    )

    #: Identifies one or more entities to which this object is attributed.
    #: The attributed entities might not be :class:`Actor`\ s.  For instance,
    #: an object might be attributed to the completion of another activity.
    attributed_to: Optional[Union[EntityRef, "Object", Link]] = (
        singular_property(
            Uri("https://www.w3.org/ns/activitystreams#attributedTo")
        )
    )

    #: Plural accessor for :attr:`attributed_to`.
    attributed_tos: Sequence[Union[EntityRef, "Object", Link]] = (
        plural_property(
            Uri("https://www.w3.org/ns/activitystreams#attributedTo")
        )
    )

    #: Identifies one or more entities that represent the total population of
    #: entities for which the object can considered to be relevant.
    audience: Optional[Union[EntityRef, "Object", Link]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#audience")
    )

    #: Plural accessor for :attr:`audience`.
    audiences: Sequence[Union[EntityRef, "Object", Link]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#audience")
    )

    #: The content or textual representation of the ``Object`` encoded as
    #: a JSON string.  By default, the value of content is HTML.
    #: The :attr:`mediaType` property can be used in the object to indicate
    #: a different content type.
    #:
    #: The content *may* be expressed using multiple language-tagged values.
    content: Optional[str | LanguageString] = singular_property(
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
    context: Optional[Union[EntityRef, "Object", Link]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#context")
    )

    #: Plural accessor for :attr:`context`.
    contexts: Sequence[Union[EntityRef, "Object", Link]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#context")
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

    #: The date and time describing the actual or expected ending time of
    #: the object.  When used with an :class:`Activity` object, for instance,
    #: the :attr:`end_time` property specifies the moment the activity
    #: concluded or is expected to conclude.
    end_time: Optional[datetime] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#endTime")
    )

    #: Identifies the entity (e.g. an application) that generated the object.
    generator: Optional[Union[EntityRef, "Object", Link]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#generator")
    )

    #: Plural accessor for :attr:`generator`.
    generators: Sequence[Union[EntityRef, "Object", Link]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#generator")
    )

    #: Indicates an entity that describes an icon for this object.
    #: The image should have an aspect ratio of one (horizontal) to
    #: one (vertical) and should be suitable for presentation at a small size.
    icon: Optional[Union["Image", Link]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#icon")
    )

    #: Plural accessor for :attr:`icon`.
    icons: Sequence[Union["Image", Link]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#icon")
    )

    #: Indicates an entity that describes an image for this object.
    #: Unlike the :attr:`icon` property, there are no aspect ratio or display
    #: size limitations assumed.
    image: Optional[Union["Image", Link]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#image")
    )

    #: Plural accessor for :attr:`image`.
    images: Sequence[Union["Image", Link]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#image")
    )

    #: Indicates one or more entities for which this object is considered
    #: a response.
    in_reply_to: Optional[Union[EntityRef, "Object", Link]] = (
        singular_property(
            Uri("https://www.w3.org/ns/activitystreams#inReplyTo")
        )
    )

    #: Plural accessor for :attr:`in_reply_to`.
    in_reply_tos: Sequence[Union[EntityRef, "Object", Link]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#inReplyTo")
    )

    #: Indicates one or more physical or logical locations associated with
    #: the object.
    location: Optional[Union[EntityRef, "Object", Link]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#location")
    )

    #: Plural accessor for :attr:`location`.
    locations: Sequence[Union[EntityRef, "Object", Link]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#location")
    )

    #: Identifies an entity that provides a preview of this object.
    preview: Optional[Union[EntityRef, Link, "Object"]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#preview")
    )

    #: Plural accessor for :attr:`preview`.
    previews: Sequence[Union[EntityRef, Link, "Object"]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#preview")
    )

    #: The date and time at which the object was published.
    published: Optional[datetime] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#published")
    )

    #: Identifies a :class:`Collection` containing objects considered to be
    #: responses to this object.
    replies: Optional[Union[EntityRef, "Collection"]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#replies")
    )

    #: The date and time describing the actual or expected starting time of
    #: the object.  When used with an :class:`Activity` object, for instance,
    #: the :attr:`start_time` property specifies the moment the activity
    #: began or is scheduled to begin.
    start_time: Optional[datetime] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#startTime")
    )

    #: A natural language summarization of the object encoded as HTML.
    #: Multiple language tagged summaries *may* be provided.
    summary: Optional[str | LanguageString] = singular_property(
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
    tag: Optional[Union[EntityRef, Link, "Object"]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#tag")
    )

    #: Plural accessor for :attr:`tag`.
    tags: Sequence[Union[EntityRef, Link, "Object"]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#tag")
    )

    #: The date and time at which the object was updated.
    updated: Optional[datetime] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#updated")
    )

    #: Identifies one or more links to representations of the object.
    url: Optional[Uri | Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#url")
    )

    #: Plural accessor for :attr:`url`.
    urls: Sequence[Uri | Link] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#url")
    )

    #: Identifies an entity considered to be part of the public primary
    #: audience of an :class:`Object`.
    to: Optional[Union[EntityRef, Link, "Object"]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#to")
    )

    #: Plural accessor for :attr:`to`.
    tos: Sequence[Union[EntityRef, Link, "Object"]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#to")
    )

    #: Identifies an entity considered to be part of the public primary
    #: audience of an :class:`Object`.
    bto: Optional[Union[EntityRef, Link, "Object"]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#bto")
    )

    #: Plural accessor for :attr:`bto`.
    btos: Sequence[Union[EntityRef, Link, "Object"]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#bto")
    )

    #: Identifies an :class:`Object` that is part of the public secondary
    #: audience of this :class:`Object`.
    cc: Optional[Union[EntityRef, Link, "Object"]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#cc")
    )

    #: Plural accessor for :attr:`cc`.
    ccs: Sequence[Union[EntityRef, Link, "Object"]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#cc")
    )

    #: Singular accessor for :attr:`bccs`.
    bcc: Optional[Union[EntityRef, Link, "Object"]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#bcc")
    )

    #: Identifies one or more :class:`Object`\ s that are part of the private
    #: secondary audience of this :class:`Object`.
    bccs: Sequence[Union[EntityRef, Link, "Object"]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#bcc")
    )

    #: Identifies the MIME media type of the value of the :attr:`content`
    #: property.  If not specified, the :attr:`content` property is assumed to
    #: contain ``text/html`` content.
    media_type: Optional[str] = singular_property(
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
    duration: Optional[Duration] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#duration")
    )

    #: The ``source`` property is intended to convey some sort of source from
    #: which the :attr:`content` markup was derived, as a form of provenance,
    #: or to support future editing by clients.  In general, clients do
    #: the conversion from ``source`` to :attr:`content`,
    #: not the other way around.
    #:
    #: The value of ``source`` is itself an object which uses its own
    # :attr:`content` and :attr:`mediaType` fields to supply source information.
    #:
    #: .. seealso::
    #:
    #:    ActivityPub --- `3.3 The source property`__
    #:
    #:    __ https://www.w3.org/TR/activitypub/#source-property
    source: Optional[Union[EntityRef, "Object"]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#source")
    )

    #: Plural accessor for :attr:`source`.
    sources: Sequence[Union[EntityRef, "Object"]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#source")
    )

    #: This is a list of all :class:`Like` activities with this object as
    #: the ``object`` property, added as a `side effect`__.  The ``likes``
    #: collection *must* be either an :class:`OrderedCollection` or
    #: a :class:`Collection` and *may* be filtered on privileges of
    #: an authenticated user or as appropriate when no authentication is given.
    #:
    #: __ https://www.w3.org/TR/activitypub/#like-activity-inbox
    #:
    #: .. note::
    #:
    #:    Care should be taken to not confuse the the :attr:`likes` collection
    #:    with the similarly named but different :attr:`~.actor.Actor.liked`
    #:    collection.  In sum:
    #:
    #:    - *liked*: Specifically a property of actors.  This is a collection
    #:      of :class:`Like` activities performed by the actor, added to
    #:      the collection as a `side effect of delivery to the outbox`__.
    #:
    #:    - *likes*:  May be a property of any object.  This is a collection
    #:      of :class:`Like` activities referencing this object, added to
    #:      the collection as a `side effect of delivery to the inbox`__.
    #:
    #:    __ https://www.w3.org/TR/activitypub/#like-activity-outbox
    #:    __ https://www.w3.org/TR/activitypub/#like-activity-inbox
    #:
    #: .. seealso::
    #:
    #:    ActivityPub --- `5.7 Likes Collection`__
    #:
    #:    __ https://www.w3.org/TR/activitypub/#likes
    likes: Optional[Union[EntityRef, "Collection"]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#likes")
    )

    #: This is a list of all :class:`Announce` activities with this object as
    #: the ``object`` property, added as a `side effect`__.  The ``shares``
    #: collection *must* be either an :class:`OrderedCollection` or
    #: a :class:`Collection` and *may* be filtered on privileges of
    #: an authenticated user or as appropriate when no authentication is given.
    #:
    #: __ https://www.w3.org/TR/activitypub/#announce-activity-inbox
    #:
    #: .. seealso::
    #:
    #:    ActivityPub --- `5.8 Shares Collection`__
    #:
    #:    __ https://www.w3.org/TR/activitypub/#shares
    shares: Optional[Union[EntityRef, "Collection"]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#shares")
    )

    #: The ``sensitive`` property on an object indicates that
    #: some users may wish to apply discretion about viewing its content,
    #: whether due to nudity, violence, or any other likely aspects that
    #: viewers may be sensitive to.  This is comparable to what is popularly
    #: called "NSFW" (Not Safe For Work) or "trigger warning" in some systems.
    #: Implementations may choose to hide content flagged with this property
    #: by default, exposed at user discretion.
    #:
    #: .. seealso::
    #:
    #:    Proposed extensions --- `as:sensitive property`__
    #:
    #:    __ https://www.w3.org/wiki/Activity_Streams_extensions#as:sensitive_property
    sensitive: Optional[bool] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#sensitive")
    )


class Article(Object):
    """Represents any kind of multi-paragraph written work."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Article")


class Event(Object):
    """Represents any kind of event."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Event")


class Note(Object):
    """Represents a short written work typically less than a single paragraph
    in length.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Note")


class Place(Object):
    """Represents a logical or physical location.  See `Activity Vocabulary 5.3
    Representing Places`__ for additional information.

    __ https://www.w3.org/TR/activitystreams-vocabulary/#places
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Place")

    #: Indicates the accuracy of position coordinates on a :class:`Place`
    #: objects.  Expressed in properties of percentage. e.g. "94.0" means
    #: "94.0% accurate".
    accuracy: Optional[float] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#accuracy")
    )

    #: Indicates the altitude of a place.  The measurement units is indicated
    #: using the :attr:`units` property.  If :attr:`units` is not specified,
    #: the default is assumed to be "``m``" indicating meters.
    altitude: Optional[float] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#altitude")
    )

    #: The latitude of a place.
    latitude: Optional[float] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#latitude")
    )

    #: The longitude of a place.
    longitude: Optional[float] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#longitude")
    )

    #: The radius from the given latitude and longitude for a :class:`Place`.
    #: The units is expressed by the :attr:`units` property.  If :attr:`units`
    #: is not specified, the default is assumed to be "``m``" indicating
    #: "meters".
    radius: Optional[float] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#radius")
    )

    #: Specifies the measurement units for the :attr:`radius` and
    #: :attr:`altitude` properties on a :class:`Place` object.
    #: If not specified, the default is assumed to be "``m``" for "meters".
    units: Optional[
        Literal["cm", "feet", "inches", "km", "m", "miles"] | Uri
    ] = singular_property(Uri("https://www.w3.org/ns/activitystreams#units"))


class Profile(Object):
    """A ``Profile`` is a content object that describes another
    :class:`Object`, typically used to describe `Actor Type`__ objects.
    The :attr:`describes` property is used to reference the object being
    described by the profile.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Profile")

    #: On a :class:`Profile` object, the describes property identifies
    #: the object described by the :class:`Profile`.
    describes: Optional[EntityRef | Object] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#describes")
    )


class Relationship(Object):
    """Describes a relationship between two individuals.  The :attr:`subject`
    and :attr:`object` properties are used to identify the connected
    individuals.

    See `Activity Vocabulary 5.2 Representing Relationships Between Entities`__
    for additional information.

    __ https://www.w3.org/TR/activitystreams-vocabulary/#connections
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Relationship")

    #: On a :class:`Relationship` object, the :attr:`subject` property
    #: identifies one of the connected individuals.  For instance,
    #: for a ``Relationship`` object describing "John is related to Sally",
    #: ``subject`` would refer to John.
    subject: Optional[EntityRef | Link | Object] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#subject")
    )

    #: Describes the entity to which the :attr:`subject` is related.
    object: Optional[EntityRef | Object | Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#object")
    )

    #: Plural accessor for :attr:`object`.
    objects: Sequence[EntityRef | Object | Link] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#object")
    )

    #: On a :class:`Relationship` object, the ``relationship`` property
    #: identifies the kind of relationship that exists between :attr:`subject`
    #: and :attr:`object`.
    #:
    #: .. note::
    #:
    #:    According to the specification, its domain is ``Object``.  However,
    #:    the example in the specification shows it can have a value of
    #:    ``xsd:anyURI``.  Hence, we use ``Object | Uri`` here.
    relationship: Optional[EntityRef | Object | Uri] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#relationship")
    )

    #: Plural accessor for :attr:`relationship`.
    relationships: Sequence[EntityRef | Object | Uri] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#relationship")
    )


class Tombstone(Object):
    r"""A ``Tombstone`` represents a content object that has been deleted.
    It can be used in :class:`Collection`\ s to signify that there used to be
    an object at this position, but it has been deleted.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Tombstone")

    #: On a :class:`Tombstone` object, the :attr:`former_type` property
    #: identifies the type of the object that was deleted.
    #:
    #: .. note::
    #:
    #:    According to the specification, its domain is ``Object``.  However,
    #:    the example in the specification shows it can have a value of
    #:    ``xsd:anyURI``.  Hence, we use ``Object | Uri`` here.
    #:
    #:    See also the `related issue`__.
    #:
    #:    __ https://github.com/w3c/activitystreams/issues/440
    former_type: Optional[EntityRef | Object | Uri] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#formerType")
    )

    #: Plural accessor for :attr:`former_type`.
    former_types: Sequence[EntityRef | Object | Uri] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#formerType")
    )

    #: On a :class:`Tombstone` object, the ``deleted`` property is a timestamp
    #: for when the object was deleted.
    deleted: Optional[datetime] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#deleted")
    )


class Hashtag(Object):
    """The ``Hashtag`` is an object type, subclass of :class:`Object`,
    which is used for hashtag-style tags under the :attr:`tag` property.

    .. seealso::

        Proposed extensions --- `as:Hashtag type`__

        __ https://www.w3.org/wiki/Activity_Streams_extensions#as:Hashtag_type
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Hashtag")


from .collection import Collection  # noqa: E402
from .document import Image  # noqa: E402
