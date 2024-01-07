from typing import TypeAlias

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


class Group(Object):
    r"""Represents a formal or informal collective of ``Actor``\ s."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Group")
    __default_context__ = Uri("https://www.w3.org/ns/activitystreams")


class Organization(Object):
    """Represents an organization."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Organization")
    __default_context__ = Uri("https://www.w3.org/ns/activitystreams")


class Person(Object):
    """Represents an individual person."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Person")
    __default_context__ = Uri("https://www.w3.org/ns/activitystreams")


class Service(Object):
    """Represents a service of any kind."""

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Service")
    __default_context__ = Uri("https://www.w3.org/ns/activitystreams")


#: Actor types are :class:`Object` types that are capable of performing
#: activities.
Actor: TypeAlias = Application | Group | Organization | Person | Service
