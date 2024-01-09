from typing import TypeAlias

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


class Application(Object):
    """Describes a software application."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Application")
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


class Group(Object):
    r"""Represents a formal or informal collective of ``Actor``\ s."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Group")
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


class Organization(Object):
    """Represents an organization."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Organization")
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


class Person(Object):
    """Represents an individual person."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Person")
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


class Service(Object):
    """Represents a service of any kind."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Service")
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


#: Actor types are :class:`Object` types that are capable of performing
#: activities.
Actor: TypeAlias = Application | Group | Organization | Person | Service
