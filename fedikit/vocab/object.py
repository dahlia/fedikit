from collections.abc import Sequence
from typing import Union

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
