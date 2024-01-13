from collections.abc import Sequence
from typing import Optional, Union

from ..model.descriptors import plural_property, singular_property
from ..uri import Uri
from .link import Link
from .object import Object

__all__ = [
    "Collection",
    "CollectionPage",
    "OrderedCollection",
    "OrderedCollectionPage",
]


class Collection(Object):
    """A ``Collection`` is a subtype of :class:`Object` that represents ordered
    or unordered sets of :class:`Object` or :class:`Link` instances.

    Refer to the `Activity Streams 2.0 Core`__ specification for a complete
    description of the ``Collection`` type.

    __ https://www.w3.org/TR/activitystreams-core/#collection
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Collection")
    __default_context__ = Uri("https://www.w3.org/ns/activitystreams")

    #: A non-negative integer specifying the total number of objects contained
    #: by the logical view of the collection.  This number might not reflect
    #: the actual number of items serialized within the :class:`Collection`
    #: object instance.
    total_items: Optional[int] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#totalItems")
    )

    #: In a paged :class:`Collection`, indicates the page that contains
    #: the most recently updated member items.
    current: Optional[Union["CollectionPage", Link]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#current")
    )

    #: In a paged :class:`Collection`, indicates the furthest preceding page of
    #: items in the collection.
    first: Optional[Union["CollectionPage", Link]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#first")
    )

    #: In a paged :class:`Collection`, indicates the furthest proceeding page
    #: of the collection.
    last: Optional[Union["CollectionPage", Link]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#last")
    )

    #: Identifies the items contained in a collection.  The items might be
    #: ordered or unordered.
    items: Sequence[Object | Link] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#items")
    )


class OrderedCollection(Collection):
    """A subtype of :class:`Collection` in which members of the logical
    collection are assumed to always be strictly ordered.
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#OrderedCollection")


class CollectionPage(Collection):
    """Used to represent distinct subsets of items from a :class:`Collection`.
    Refer to the `Activity Streams 2.0 Core`__ for a complete description of
    the ``CollectionPage`` object.

    __ https://www.w3.org/TR/activitystreams-core/#dfn-collectionpage
    """

    __uri__ = Uri("https://www.w3.org/ns/activitystreams#CollectionPage")

    #: Identifies the :class:`Collection` to which a :class:`CollectionPage`
    #: objects items belong.
    part_of: Optional[Link | Collection] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#partOf")
    )

    #: In a paged :class:`Collection`, indicates the next page of items.
    next: Optional[Union["CollectionPage", Link]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#next")
    )

    #: In a paged :class:`Collection`, identifies the previous page of items.
    prev: Optional[Union["CollectionPage", Link]] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#prev")
    )


class OrderedCollectionPage(OrderedCollection, CollectionPage):
    """Used to represent ordered subsets of items from
    an :class:`OrderedCollection`.  Refer to the `Activity Streams 2.0 Core`
    for a complete description of the ``OrderedCollectionPage`` object.

    __ https://www.w3.org/TR/activitystreams-core/#dfn-orderedcollectionpage
    """
