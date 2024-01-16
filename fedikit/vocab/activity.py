from collections.abc import Sequence
from typing import Optional

from ..model.descriptors import plural_property, singular_property
from ..model.entity import EntityRef
from ..uri import Uri
from .link import Link
from .object import Object

__all__ = [
    "Accept",
    "Activity",
    "Add",
    "Announce",
    "Block",
    "Create",
    "Delete",
    "Dislike",
    "Flag",
    "Follow",
    "Ignore",
    "Invite",
    "Join",
    "Leave",
    "Like",
    "Listen",
    "Move",
    "Offer",
    "Reject",
    "Read",
    "Remove",
    "TentativeAccept",
    "TentativeReject",
    "Undo",
    "Update",
    "View",
]


class Activity(Object):
    """An ``Activity`` is a subtype of :class:`Object` that describes some form
    of action that may happen, is currently happening, or has already happened.
    The ``Activity`` type itself serves as an abstract base type for all types
    of activities.  It is important to note that the ``Activity`` type itself
    does not carry any specific semantics about the kind of action being taken.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Activity")
    __default_context__ = Uri("https://www.w3.org/ns/activitystreams")

    #: Describes one or more entities that either performed or are expected to
    #: perform the activity.  Any single activity can have multiple
    #: ``actor``\ s.  The ``actor`` *may* be specified using an indirect
    #: :class:`Link`.
    actor: Optional[EntityRef | Object | Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#actor")
    )

    #: Plural accessor for :attr:`actor`.
    actors: Sequence[EntityRef | Object | Link] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#actor")
    )

    #: Identifies one or more entities to which this object is attributed.
    #: The attributed entities might not be :class:`Actor`\ s.  For instance,
    #: an object might be attributed to the completion of another activity.
    attributed_to: Optional[EntityRef | Object | Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#attributedTo"),
        subproperties=[Uri("https://www.w3.org/ns/activitystreams#actor")],
    )

    #: Plural accessor for :attr:`attributed_to`.
    attributed_tos: Sequence[EntityRef | Object | Link] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#attributedTo"),
        subproperties=[Uri("https://www.w3.org/ns/activitystreams#actor")],
    )

    #: Describes the direct object of the activity.  For instance, in the
    #: activity "John added a movie to his wishlist", the object of
    #: the activity is the movie added.
    object: Optional[EntityRef | Object | Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#object")
    )

    #: Plural accessor for :attr:`object`.
    objects: Sequence[EntityRef | Object | Link] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#object")
    )

    #: Describes the indirect object, or target, of the activity.  The precise
    #: meaning of the target is largely dependent on the type of action being
    #: described but will often be the object of the English preposition "to".
    #: For instance, in the activity "John added a movie to his wishlist",
    #: the target of the activity is John's wishlist.  An activity can have
    #: more than one target.
    target: Optional[EntityRef | Object | Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#target")
    )

    #: Plural accessor for :attr:`target`.
    targets: Sequence[EntityRef | Object | Link] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#target")
    )

    #: Describes the result of the activity.  For instance, if a particular
    #: action results in the creation of a new resource, the result property
    #: can be used to describe that new resource.
    result: Optional[EntityRef | Object | Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#result")
    )

    #: Plural accessor for :attr:`result`.
    results: Sequence[EntityRef | Object | Link] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#result")
    )

    #: Describes an indirect object of the activity from which the activity
    #: is directed.  The precise meaning of the origin is the object of
    #: the English preposition "from".  For instance, in the activity
    #: "John moved an item to List B from List A", the origin of the activity
    #: is "List A".
    origin: Optional[EntityRef | Object | Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#origin")
    )

    #: Plural accessor for :attr:`origin`.
    origins: Sequence[EntityRef | Object | Link] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#origin")
    )

    #: Identifies one or more objects used (or to be used) in the completion of
    #: an :class:`Activity`.
    instrument: Optional[EntityRef | Object | Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#instrument")
    )

    #: Plural accessor for :attr:`instrument`.
    instruments: Sequence[EntityRef | Object | Link] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#instrument")
    )


class Accept(Activity):
    """Indicates that the :attr:`actor` accepts the :attr:`object`.
    The :attr:`target` property can be used in certain circumstances to
    indicate the context into which the :attr:`object` has been accepted.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Accept")


class Add(Activity):
    """Indicates that the :attr:`actor` has added the :attr:`object` to
    the :attr:`target`.  If the :attr:`target` property is not explicitly
    specified, the target would need to be determined implicitly by context.
    The :attr:`origin` can be used to identify the context from which
    the :attr:`object` originated.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Add")


class Announce(Activity):
    """Indicates that the :attr:`actor` is calling the :attr:`target`'s
    attention the :attr:`object`.

    The :attr:`origin` typically has no defined meaning.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Announce")


class Create(Activity):
    """Indicates that the :attr:`actor` has created the :attr:`object`."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Create")


class Delete(Activity):
    """Indicates that the :attr:`actor` has deleted the object.  If specified,
    the :attr:`origin` indicates the context from which the :attr:`object` was
    deleted.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Delete")


class Dislike(Activity):
    """Indicates that the :attr:`actor` dislikes the :attr:`object`."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Dislike")


class Flag(Activity):
    """Indicates that the :attr:`actor` is "flagging" the :attr:`object`.
    Flagging is defined in the sense common to many social platforms as
    reporting content as being inappropriate for any number of reasons.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Flag")


class Follow(Activity):
    """Indicates that the :attr:`actor` is "following" the :attr:`object`.
    Following is defined in the sense typically used within social systems
    in which the actor is interested in any activity performed by or
    on the object.  The :attr:`target` and :attr:`origin` typically have
    no defined meaning.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Follow")


class Ignore(Activity):
    """Indicates that the :attr:`actor` is ignoring the :attr:`object`.
    The :attr:`target` and :attr:`origin` typically have no defined meaning.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Ignore")


class Block(Ignore):
    """Indicates that the :attr:`actor` is blocking the :attr:`object`.
    Blocking is a stronger form of :class:`Ignore`. The typical use is to
    support social systems that allow one user to block activities or content
    of other users.  The :attr:`target` and :attr:`origin` typically have
    no defined meaning.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Block")


class Join(Activity):
    """Indicates that the :attr:`actor` has joined the :attr:`object`.
    The :attr:`target` and :attr:`origin` typically have no defined meaning.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Join")


class Leave(Activity):
    """Indicates that the :attr:`actor` has left the :attr:`object`.
    The :attr:`target` and :attr:`origin` typically have no meaning.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Leave")


class Like(Activity):
    """Indicates that the :attr:`actor` likes, recommends or endorses
    the :attr:`object`.  The :attr:`target` and :attr:`origin` typically have
    no defined meaning.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Like")


class Listen(Activity):
    """Indicates that the :attr:`actor` has listened to the :attr:`object`."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Listen")


class Move(Activity):
    """Indicates that the :attr:`actor` has moved :attr:`object` from
    :attr:`origin` to :attr:`target`. If the :attr:`origin` or :attr:`target`
    are not specified, either can be determined by context.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Move")


class Offer(Activity):
    """Indicates that the :attr:`actor` is offering the :attr:`object`.
    If specified, the :attr:`target` indicates the entity to which
    the :attr:`object` is being offered.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Offer")


class Invite(Offer):
    """A specialization of :class:`Offer` in which the :attr:`actor` is
    extending an invitation for the :attr:`object` to the :attr:`target`.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Invite")


class Reject(Activity):
    """Indicates that the :attr:`actor` is rejecting the :attr:`object`.
    The :attr:`target` and :attr:`origin` typically have no defined meaning.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Reject")


class Read(Activity):
    """Indicates that the :attr:`actor` has read the :attr:`object`."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Read")


class Remove(Activity):
    """Indicates that the :attr:`actor` is removing the :attr:`object`.
    If specified, the :attr:`origin` indicates the context from which
    the :attr:`object` is being removed.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Remove")


class TentativeReject(Reject):
    """A specialization of :class:`Reject` in which the rejection is
    considered tentative.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#TentativeReject")


class TentativeAccept(Accept):
    """A specialization of :class:`Accept` in which the acceptance is
    considered tentative.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#TentativeAccept")


class Undo(Activity):
    """Indicates that the :attr:`actor` is undoing the :attr:`object`.
    In most cases, the :attr:`object` will be an :class:`Activity` describing
    some previously performed action (for instance, a person may have
    previously "liked" an article but, for whatever reason, might choose to
    undo that like at some later point in time).

    The :attr:`target` and :attr:`origin` typically have no defined meaning.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Undo")


class Update(Activity):
    """Indicates that the :attr:`actor` has updated the :attr:`object`.
    Note, however, that this vocabulary does not define a mechanism for
    describing the actual set of modifications made to :attr:`object`.

    The :attr:`target` and :attr:`origin` typically have no defined meaning.
    """


class View(Activity):
    """Indicates that the :attr:`actor` has viewed the object."""
