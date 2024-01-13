from collections.abc import Sequence
from typing import Optional

from ..model.descriptors import plural_property, singular_property
from ..model.entity import Entity
from ..model.langstr import LanguageString
from ..uri import Uri
from .collection import Collection, OrderedCollection
from .object import Object

__all__ = [
    "Actor",
    "Application",
    "Endpoints",
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

    #: The inbox stream contains all activities received by the actor.
    #: The server *should* filter content according to the requester's
    #: permission.  In general, the owner of an inbox is likely to be able to
    #: access all of their inbox contents.  Depending on access control,
    #: some other content may be public, whereas other content may require
    #: authentication for non-owner users, if they can access the inbox at all.
    #
    #: The server *must* perform de-duplication of activities returned by
    #: the inbox.  Duplication can occur if an activity is addressed both to
    #: an actor's followers, and a specific actor who also follows the recipient
    #: actor, and the server has failed to de-duplicate the recipients list.
    #: Such deduplication *must* be performed by comparing the ``id`` of
    #: the activities and dropping any activities already seen.
    #:
    #: .. seealso::
    #:
    #:    ActivityPub --- `5.2 Inbox`__
    #:
    #:    __ https://www.w3.org/TR/activitypub/#inbox
    inbox: Optional[OrderedCollection] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#inbox")
    )

    #: The outbox stream contains activities the user has published,
    #: subject to the ability of the requestor to retrieve the activity
    #: (that is, the contents of the outbox are filtered by the permissions of
    #: the person reading it).  If a user submits a request without
    #: authorization__ the server should respond with all of the Public__ posts.
    #: This could potentially be all relevant objects published by the user,
    #: though the number of available items is left to the discretion of
    #: those implementing and deploying the server.
    #:
    #: __ https://www.w3.org/TR/activitypub/#authorization
    #: __ https://www.w3.org/TR/activitypub/#public-addressing
    #:
    #: .. seealso::
    #:
    #:    ActivityPub --- `5.1 Outbox`__
    #:
    #:    __ https://www.w3.org/TR/activitypub/#outbox
    outbox: Optional[OrderedCollection] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#outbox")
    )

    #: This is a list of everybody that the actor has followed, added as
    #: a `side effect`__.  The ``following`` collection *must* be either
    #: an :class:`OrderedCollection` or a :class:`Collection` and *may* be
    #: filtered on privileges of an authenticated user or as appropriate
    #: when no authentication is given.
    #:
    #: __ https://www.w3.org/TR/activitypub/#follow-activity-outbox
    #:
    #: .. seealso::
    #:
    #:    ActivityPub --- `5.4 Following Collection`__
    #:
    #:    __ https://www.w3.org/TR/activitypub/#following
    following: Optional[Collection] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#following")
    )

    #: This is a list of everyone who has sent a :class:`Follow` activity for
    #: the actor, added as a `side effect`__.  This is where one would find
    #: a list of all the actors that are following the actor.  The ``followers``
    #: collection *must* be either an :class:`OrderedCollection` or
    #: a :class:`Collection` and *may* be filtered on privileges of
    #: an authenticated user or as appropriate when no authentication is given.
    #:
    #: __ https://www.w3.org/TR/activitypub/#follow-activity-outbox
    #:
    #: .. seealso::
    #:
    #:    ActivityPub --- `5.3 Followers Collection`__
    #:
    #:    __ https://www.w3.org/TR/activitypub/#followers
    followers: Optional[Collection] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#followers")
    )

    #: This is a list of every object from all of the actor's :class:`Like`
    #: activities, added as a `side effect`__.  The ``liked`` collection *must*
    #: be either an :class:`OrderedCollection` or a :class:`Collection` and
    #: *may* be filtered on privileges of an authenticated user or as
    #: appropriate when no authentication is given.
    #:
    #: __ https://www.w3.org/TR/activitypub/#like-activity-outbox
    #:
    #: .. seealso::
    #:
    #:    ActivityPub --- `5.5 Liked Collection`__
    #:
    #:    __ https://www.w3.org/TR/activitypub/#liked
    liked: Optional[Collection] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#liked")
    )

    #: A list of supplementary Collections which may be of interest.
    #:
    #: .. seealso::
    #:
    #:    ActivityPub --- `4.1 Actor objects`__
    #:
    #:    __ https://www.w3.org/TR/activitypub/#actor-objects
    streams: Sequence[Collection] = plural_property(
        Uri("https://www.w3.org/ns/activitystreams#streams")
    )

    #: A short username which may be used to refer to the actor,
    #: with no uniqueness guarantees.
    #:
    #: .. seealso::
    #:
    #:    ActivityPub --- `4.1 Actor objects`__
    #:
    #:    __ https://www.w3.org/TR/activitypub/#actor-objects
    preferred_username: Optional[str | LanguageString] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#preferredUsername")
    )

    #: A JSON object which maps additional (typically server/domain-wide)
    #: endpoints which may be useful either for this actor or someone
    #: referencing this actor.  This mapping may be nested inside the actor
    #: document as the value or may be a link to a JSON-LD document with
    #: these properties.
    #:
    #: .. seealso::
    #:
    #:    ActivityPub --- `4.1 Actor objects`__
    #:
    #:    __ https://www.w3.org/TR/activitypub/#actor-objects
    endpoints: Optional["Endpoints"] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#endpoints")
    )

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
    manually_approves_followers: Optional[bool] = singular_property(
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


class Endpoints(Entity):
    """Contents of :attr:`Actor.endpoints`.

    .. seealso::

        ActivityPub --- `4.1 Actor objects`__

        __ https://www.w3.org/TR/activitypub/#actor-objects
    """

    __abstract__ = False
    __uri__ = Uri("https://www.w3.org/ns/activitystreams#Endpoints")

    #: Endpoint URI so this actor's clients may access remote ActivityStreams
    #: objects which require authentication to access.  To use this endpoint,
    #: the client posts an ``x-www-form-urlencoded`` ``id`` parameter with
    #: the value being the ``id`` of the requested ActivityStreams object.
    proxy_url: Optional[Uri] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#proxyUrl")
    )

    #: If OAuth 2.0 bearer tokens [:rfc:`6749`] [:rfc:`6750`] are being used for
    #: authenticating `client to server interactions`__, this endpoint specifies
    #: a URI at which a browser-authenticated user may obtain
    #: a new authorization grant.
    #:
    #: __ https://www.w3.org/TR/activitypub/#client-to-server-interactions
    oauth_authorization_endpoint: Optional[Uri] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#oauthAuthorizationEndpoint")
    )

    #: If OAuth 2.0 bearer tokens [:rfc:`6749`] [:rfc:`6750`] are being used for
    #: authenticating `client to server interactions`__, this endpoint specifies
    #: a URI at which a client may acquire an access token.
    #:
    #: __ https://www.w3.org/TR/activitypub/#client-to-server-interactions
    oauth_token_endpoint: Optional[Uri] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#oauthTokenEndpoint")
    )

    #: If Linked Data Signatures and HTTP Signatures are being used for
    #: authentication and authorization, this endpoint specifies a URI at which
    #: browser-authenticated users may authorize a client's public key for
    #: `client to server interactions`__.
    #:
    #: __ https://www.w3.org/TR/activitypub/#client-to-server-interactions
    provide_client_key: Optional[Uri] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#provideClientKey")
    )

    #: If Linked Data Signatures and HTTP Signatures are being used for
    #: authentication and authorization, this endpoint specifies a URI at which
    #: a client key may be signed by the actor's key for a time window to act
    #: on behalf of the actor in interacting with foreign servers.
    sign_client_key: Optional[Uri] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#signClientKey")
    )

    #: An optional endpoint `used for wide delivery of publicly addressed
    #: activities and activities sent to followers`__.
    #: ``sharedInbox`` endpoints *should* also be publicly readable
    #: :class:`OrderedCollection` objects containing objects addressed to
    #: the Public__ special collection.  Reading from the ``sharedInbox``
    #: endpoint *must not* present objects which are not addressed to
    #: the ``Public`` endpoint.
    #:
    #: __ https://www.w3.org/TR/activitypub/#shared-inbox-delivery
    #: __ https://www.w3.org/TR/activitypub/#public-addressing
    shared_box: Optional[Uri] = singular_property(
        Uri("https://www.w3.org/ns/activitystreams#sharedInbox")
    )
