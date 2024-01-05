from collections.abc import Sequence

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
