from collections.abc import Sequence
from datetime import datetime
from typing import Optional

from ..model.descriptors import plural_property, singular_property
from ..uri import Uri
from .activity import Activity
from .link import Link
from .object import Object

__all__ = ["Arrive", "IntransitiveActivity", "Question"]


class IntransitiveActivity(Activity):
    """Instances of ``IntransitiveActivity`` are a subtype of Activity
    representing intransitive actions. The :attr:`object` property is therefore
    inappropriate for these activities.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#IntransitiveActivity")


class Arrive(IntransitiveActivity):
    """An :class:`IntransitiveActivity` that indicates that the :attr:`actor`
    has arrived at the :attr:`location`.  The :attr:`origin` can be used to
    identify the context from which the :attr:`actor` originated.
    The :attr:`target` typically has no defined meaning.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Arrive")


class Question(IntransitiveActivity):
    """Represents a question being asked.  Question objects are an extension of
    :class:`IntransitiveActivity`.  That is, the ``Question`` object is an
    :class:`Activity`, but the direct object is the question itself and
    therefore it would not contain an :attr:`object` property.

    Either of the :attr:`any_of` and :attr:`one_of` properties *may* be used to
    express possible answers, but a ``Question`` object *must not* have both
    properties.
    """

    #: Identifies an exclusive option for a :class:`Question`.
    #: Use of ``one_of`` implies that the :class:`Question` can have only
    #: a single answer.  To indicate that a :class:`Question` can have multiple
    #: answers, use :attr:`any_of`.
    one_of: Sequence[Object | Link] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#oneOf")
    )

    #: Identifies an inclusive option for a :class:`Question`.
    #: Use of ``any_of`` implies that the :class:`Question` can have multiple
    #: answers.  To indicate that a :class:`Question` can have only one answer,
    #: use :attr:`one_of`.
    any_of: Sequence[Object | Link] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#anyOf")
    )

    #: Indicates that a question has been closed, and answers are no longer
    #: accepted.
    closed: Optional[Object | Link | datetime | bool] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#closed")
    )

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Question")
