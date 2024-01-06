from collections.abc import Sequence
from typing import Union

from ..model.descriptors import plural_property, singular_property
from ..model.entity import Uri
from .link import Link
from .object import Object

__all__ = ["Activity"]


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
    actor: Union["Object", Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#actor")
    )

    #: Plural accessor for :attr:`actor`.
    actors: Sequence[Union["Object", Link]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#actor")
    )

    #: Identifies one or more entities to which this object is attributed.
    #: The attributed entities might not be :class:`Actor`\ s.  For instance,
    #: an object might be attributed to the completion of another activity.
    attributed_to: Union["Object", Link] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#attributedTo"),
        subproperties=[Uri("https://www.w3.org/ns/activitystreams#actor")],
    )

    #: Plural accessor for :attr:`attributed_to`.
    attributed_tos: Sequence[Union["Object", Link]] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#attributedTo"),
        subproperties=[Uri("https://www.w3.org/ns/activitystreams#actor")],
    )

    #: Describes the direct object of the activity.  For instance, in the
    #: activity "John added a movie to his wishlist", the object of
    #: the activity is the movie added.
    object: Object | Link = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#object")
    )

    #: Plural accessor for :attr:`object`.
    objects: Sequence[Object | Link] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#object")
    )
