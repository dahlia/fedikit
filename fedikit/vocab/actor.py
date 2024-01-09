from ..model.descriptors import singular_property
from ..model.entity import Uri
from .object import Object

__all__ = [
    "Actor",
    "Application",
    "Group",
    "Organization",
    "Person",
    "Service",
]


class Actor(Object):
    """Actor types are :class:`Object` types that are capable of performing
    activities.
    """

    __abstract__ = True
    __default_context__ = Uri("https://www.w3.org/ns/activitystreams")

    #: When ``true``, conveys that for this actor, follow requests are not
    #: usually automatically approved, but instead are examined by a person
    #: who may accept or reject the request, at some time in the future.
    #: Setting of ``false`` conveys no information and may be ignored.
    #: This information is typically used to affect display of accounts,
    #: such as showing an account as private or locked.
    #:
    #: .. seealso::
    #:
    #:    Proposed extensions --- `as:manuallyApprovesFollowers`__
    #:
    #:    __ https://www.w3.org/wiki/Activity_Streams_extensions#as:manuallyApprovesFollowers
    manually_approves_followers: bool = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#manuallyApprovesFollowers")
    )


class Application(Actor):
    """Describes a software application."""

    __abstract__ = False
    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Application")


class Group(Actor):
    r"""Represents a formal or informal collective of ``Actor``\ s."""

    __abstract__ = False
    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Group")


class Organization(Actor):
    """Represents an organization."""

    __abstract__ = False
    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Organization")


class Person(Actor):
    """Represents an individual person."""

    __abstract__ = False
    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Person")


class Service(Actor):
    """Represents a service of any kind."""

    __abstract__ = False
    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Service")
