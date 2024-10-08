import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import (
    Any,
    Awaitable,
    Callable,
    Generic,
    Optional,
    Protocol,
    Self,
    TypeAlias,
    TypeVar,
)
from urllib.parse import quote

from hypercorn.typing import ASGIReceiveCallable, ASGISendCallable, Scope
from werkzeug.datastructures import Headers
from werkzeug.exceptions import MethodNotAllowed, NotFound
from werkzeug.routing import Map, MapAdapter, Rule
from werkzeug.sansio.request import Request

from ..model.converters import jsonld
from ..model.entity import EntityRef
from ..uri import Uri
from ..vocab import link
from ..vocab.activity import Activity
from ..vocab.actor import Actor
from ..vocab.collection import OrderedCollection, OrderedCollectionPage
from ..webfinger.jrd import Link, MediaType, ResourceDescriptor
from .collection import Page

__all__ = [
    "ActorDispatcher",
    "AsgiApp",
    "Context",
    "OutboxCounter",
    "OutboxDispatcher",
    "Request",
    "Server",
    "ServerAsgi",
]


#: A type alias for an ASGI application.
AsgiApp: TypeAlias = Callable[
    [
        Scope,
        ASGIReceiveCallable,
        ASGISendCallable,
    ],
    Awaitable[None],
]


async def non_http(
    scope: Scope,
    receive: ASGIReceiveCallable,
    send: ASGISendCallable,
) -> None:
    raise NotImplementedError(f"Unknown scope type: {scope['type']}")


async def not_found(
    scope: Scope,
    receive: ASGIReceiveCallable,
    send: ASGISendCallable,
) -> None:
    await send({
        "type": "http.response.start",
        "status": 404,
        "headers": [(b"content-type", b"text/plain")],
    })
    await send({
        "type": "http.response.body",
        "body": b"Not Found",
        "more_body": False,
    })


async def method_not_allowed(
    scope: Scope,
    receive: ASGIReceiveCallable,
    send: ASGISendCallable,
) -> None:
    await send({
        "type": "http.response.start",
        "status": 405,
        "headers": [(b"content-type", b"text/plain")],
    })
    await send({
        "type": "http.response.body",
        "body": b"Method Not Allowed",
        "more_body": False,
    })


async def not_acceptable(
    scope: Scope,
    receive: ASGIReceiveCallable,
    send: ASGISendCallable,
) -> None:
    await send({
        "type": "http.response.start",
        "status": 406,
        "headers": [(b"content-type", b"text/plain")],
    })
    await send({
        "type": "http.response.body",
        "body": b"Not Acceptable",
        "more_body": False,
    })


TContextData = TypeVar("TContextData")


@dataclass(frozen=True)
class Context(Generic[TContextData]):
    """A context for a request."""

    #: The request object.
    request: Request

    #: The routing map adapter.
    map_adapter: MapAdapter

    #: The user-defined context data.
    data: TContextData

    def actor_uri(self, handle: str) -> Uri:
        """Return the URI of an actor with the given handle.

        :param handle: The actor's handle.
        :return: The actor's URI.

        """
        return Uri(
            self.map_adapter.build(
                "actor", {"handle": handle}, force_external=True
            )
        )

    def outbox_uri(self, handle: str) -> Uri:
        """Return the URI of an actor's outbox with the given handle.

        :param handle: The actor's handle.
        :return: The actor's outbox URI.

        """
        return Uri(
            self.map_adapter.build(
                "outbox", {"handle": handle}, force_external=True
            )
        )


class ActorDispatcher(Protocol[TContextData]):
    """A protocol for callables that dispatch actors."""

    def __call__(
        self, context: Context[TContextData], handle: str
    ) -> Optional[Actor] | Awaitable[Optional[Actor]]: ...


class OutboxDispatcher(Protocol[TContextData]):
    """A protocol for callables that dispatch outboxes."""

    def __call__(
        self,
        context: Context[TContextData],
        handle: str,
        cursor: Optional[str],
    ) -> Optional[Page[Activity]] | Awaitable[Optional[Page[Activity]]]: ...


class OutboxCounter(Protocol[TContextData]):
    """A protocol for callables that count outbox contents."""

    def __call__(
        self,
        context: Context[TContextData],
        handle: str,
    ) -> Optional[int] | Awaitable[Optional[int]]: ...


class OutboxCursor(Protocol[TContextData]):
    """A protocol for callables that return a cursor for an outbox."""

    def __call__(
        self,
        context: Context[TContextData],
        handle: str,
    ) -> Optional[str] | Awaitable[Optional[str]]: ...


class Server(Generic[TContextData]):
    """A server to handle requests from the fediverse."""

    _map: Map
    _actor_dispatcher: Optional[ActorDispatcher[TContextData]]
    _outbox_dispatcher: Optional[OutboxDispatcher[TContextData]]
    _outbox_counter: Optional[OutboxCounter[TContextData]]
    _outbox_first_cursor: Optional[OutboxCursor[TContextData]]
    _outbox_last_cursor: Optional[OutboxCursor[TContextData]]

    def __init__(self) -> None:
        self._map = Map([
            Rule("/.well-known/webfinger", endpoint="webfinger"),
        ])
        self._actor_dispatcher = None
        self._outbox_dispatcher = None
        self._outbox_counter = None
        self._outbox_first_cursor = None
        self._outbox_last_cursor = None

    def clone(self) -> Self:
        """Copy the server.

        :return: A copy of the server.
        """
        clone = type(self)()
        clone._map = Map(rule.empty() for rule in self._map.iter_rules())
        clone._actor_dispatcher = self._actor_dispatcher
        clone._outbox_dispatcher = self._outbox_dispatcher
        clone._outbox_counter = self._outbox_counter
        clone._outbox_first_cursor = self._outbox_first_cursor
        clone._outbox_last_cursor = self._outbox_last_cursor
        return clone

    def actor_dispatcher(
        self, path: str
    ) -> Callable[
        [ActorDispatcher[TContextData]], ActorDispatcher[TContextData]
    ]:
        """A decorator to register an actor dispatcher.

        :param path: The path to route to the actor dispatcher.  It must contain
            a ``<handle>`` placeholder.
        """
        rule = Rule(path, endpoint="actor")

        def decorate(
            dispatch: ActorDispatcher[TContextData],
        ) -> ActorDispatcher[TContextData]:
            self._actor_dispatcher = dispatch
            self._map.add(rule)
            return dispatch

        return decorate

    def outbox_dispatcher(
        self, path: str
    ) -> Callable[
        [OutboxDispatcher[TContextData]], OutboxDispatcher[TContextData]
    ]:
        """A decorator to register an outbox dispatcher.

        :param path: The path to route to the outbox dispatcher.  It must
            contain a ``<handle>`` placeholder.
        """
        rule = Rule(path, endpoint="outbox")

        def decorate(
            dispatch: OutboxDispatcher[TContextData],
        ) -> OutboxDispatcher[TContextData]:
            self._outbox_dispatcher = dispatch
            self._map.add(rule)
            return dispatch

        return decorate

    def outbox_counter(
        self, count: OutboxCounter[TContextData]
    ) -> OutboxCounter[TContextData]:
        """A decorator to register an outbox counter."""
        self._outbox_counter = count
        return count

    def outbox_first_cursor(
        self, cursor: OutboxCursor[TContextData]
    ) -> OutboxCursor[TContextData]:
        """A decorator to register an outbox first cursor."""
        self._outbox_first_cursor = cursor
        return cursor

    def outbox_last_cursor(
        self, cursor: OutboxCursor[TContextData]
    ) -> OutboxCursor[TContextData]:
        """A decorator to register an outbox last cursor."""
        self._outbox_last_cursor = cursor
        return cursor

    async def dispatch_actor(
        self, context: Context[TContextData], handle: str
    ) -> Optional[Actor]:
        """Dispatch an actor using the registered actor dispatcher.

        :param context: The context for the request.
        :param handle: The actor's handle to dispatch.
        :return: The actor, or ``None`` if no actor was found.
        """
        if self._actor_dispatcher is None:
            return None
        dispatched = self._actor_dispatcher(context, handle)
        if dispatched is None or isinstance(dispatched, Actor):
            return dispatched
        return await dispatched

    async def dispatch_outbox(
        self,
        context: Context[TContextData],
        handle: str,
        cursor: Optional[str],
    ) -> Optional[Page[Activity]]:
        """Dispatch an outbox using the registered outbox dispatcher.

        :param context: The context for the request.
        :param handle: The actor's handle whose outbox to dispatch.
        :param cursor: An optional cursor to paginate the outbox.
        :return: The contents of the outbox, or ``None`` if no outbox was found.
        """
        if self._outbox_dispatcher is None:
            return None
        dispatched = self._outbox_dispatcher(context, handle, cursor)
        if dispatched is None or isinstance(dispatched, Page):
            return dispatched
        return await dispatched

    async def count_outbox(
        self, context: Context[TContextData], handle: str
    ) -> Optional[int]:
        """Count the contents of an outbox using the registered outbox counter.

        :param context: The context for the request.
        :param handle: The actor's handle whose outbox to count.
        :return: The number of items in the outbox, or ``None`` if no outbox was
            found or the outbox has no counter.
        """
        if self._outbox_counter is None:
            return None
        total_items = self._outbox_counter(context, handle)
        if total_items is None or isinstance(total_items, int):
            return total_items
        return await total_items

    async def get_outbox_first_cursor(
        self, context: Context[TContextData], handle: str
    ) -> Optional[str]:
        """Get the first cursor of an outbox using the registered outbox first cursor.

        :param context: The context for the request.
        :param handle: The actor's handle whose outbox to get the first cursor.
        :return: The first cursor of the outbox, or ``None`` if no outbox was
            found or the outbox has no first cursor.
        """
        if self._outbox_first_cursor is None:
            return None
        cursor = self._outbox_first_cursor(context, handle)
        if cursor is None or isinstance(cursor, str):
            return cursor
        return await cursor

    async def get_outbox_last_cursor(
        self, context: Context[TContextData], handle: str
    ) -> Optional[str]:
        """Get the last cursor of an outbox using the registered outbox last cursor.

        :param context: The context for the request.
        :param handle: The actor's handle whose outbox to get the last cursor.
        :return: The last cursor of the outbox, or ``None`` if no outbox was
            found or the outbox has no last cursor.
        """
        if self._outbox_last_cursor is None:
            return None
        cursor = self._outbox_last_cursor(context, handle)
        if cursor is None or isinstance(cursor, str):
            return cursor
        return await cursor

    def asgi(
        self,
        context: TContextData,
        on_non_http: AsgiApp = non_http,
        on_not_found: AsgiApp = not_found,
        on_method_not_allowed: AsgiApp = method_not_allowed,
        on_not_acceptable: AsgiApp = not_acceptable,
    ) -> "ServerAsgi[TContextData]":
        """Return an ASGI application.

        :param context: The user-defined context data.
        :param on_non_http: The ASGI application to call if the scope is not
            ``http``.  If omitted, a :exc:`NotImplementedError` is raised in
            this case.
        :param on_not_found: The ASGI application to call if the request was
            not found.  If omitted, a 404 response is returned in this case.
        :param on_method_not_allowed: The ASGI application to call if the
            request method is not allowed.  If omitted, a 405 response is
            returned in this case.
        :param on_not_acceptable: The ASGI application to call if the request
            does not accept the response media type.  If omitted, a 406
            response is returned in this case.
        """
        return ServerAsgi[TContextData](
            self,
            context,
            on_non_http,
            on_not_found,
            on_method_not_allowed,
            on_not_acceptable,
        )


class ServerAsgi(Generic[TContextData]):
    """An ASGI application for a :class:`Server`.  Usually instantiated by
    :meth:`Server.asgi()` method.
    """

    server: Server[TContextData]
    context_data: TContextData
    on_non_http: AsgiApp
    on_not_found: AsgiApp
    on_method_not_allowed: AsgiApp
    on_not_acceptable: AsgiApp

    def __init__(
        self,
        server: Server[TContextData],
        context_data: TContextData,
        on_non_http: AsgiApp = non_http,
        on_not_found: AsgiApp = not_found,
        on_method_not_allowed: AsgiApp = method_not_allowed,
        on_not_acceptable: AsgiApp = not_acceptable,
    ) -> None:
        self.server = server
        self.context_data = context_data
        self.on_non_http = on_non_http
        self.on_not_found = on_not_found
        self.on_method_not_allowed = on_method_not_allowed
        self.on_not_acceptable = on_not_acceptable

    async def __call__(
        self,
        scope: Scope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ) -> None:
        if scope["type"] != "http":
            return await self.on_non_http(scope, receive, send)
        url_scheme = scope["scheme"]
        server = scope["server"]
        if server is None:
            server_name = None
        elif (
            url_scheme == "http"
            and server[1] == 80
            or url_scheme == "https"
            and server[1] == 443
        ):
            server_name = server[0]
        else:
            server_name = "{0}:{1}".format(*server)
        script_name = scope["root_path"]
        method = scope["method"]
        path_info = scope["path"][len(script_name) :]
        query_string = scope["query_string"].decode("ascii")
        headers = Headers(
            (k.decode("ascii"), v.decode("ascii")) for k, v in scope["headers"]
        )
        adapter = self.server._map.bind(
            headers.get("Host", server_name) or "",
            script_name,
            url_scheme=url_scheme,
            default_method=method,
            path_info=path_info,
            query_args=query_string,
        )
        try:
            endpoint, args = adapter.match()
        except NotFound:
            return await self.on_not_found(scope, receive, send)
        except MethodNotAllowed:
            return await self.on_method_not_allowed(scope, receive, send)
        request = Request(
            method,
            url_scheme,
            scope["server"],
            script_name,
            path_info,
            scope["query_string"],
            headers,
            scope["client"] and scope["client"][0],
        )
        if not (
            len(request.accept_mimetypes) < 1
            or "application/ld+json" in request.accept_mimetypes  # type: ignore
            or "application/activity+json" in request.accept_mimetypes  # type: ignore
            or "application/json" in request.accept_mimetypes  # type: ignore
        ):
            return await self.on_not_acceptable(scope, receive, send)
        context = Context(request, adapter, self.context_data)
        match endpoint:
            case "webfinger":
                return await self._webfinger_asgi(
                    context, args, scope, receive, send
                )
            case "actor":
                return await self._actor_asgi(
                    context, args, scope, receive, send
                )
            case "outbox":
                return await self._outbox_asgi(
                    context, args, scope, receive, send
                )
        return await self.on_not_found(scope, receive, send)

    async def _webfinger_asgi(
        self,
        context: Context[TContextData],
        args: Mapping[str, Any],
        scope: Scope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ) -> None:
        if self.server._actor_dispatcher is None:
            return await self.on_not_found(scope, receive, send)
        resource = context.request.args.get("resource")
        if resource is None:
            await send({
                "type": "http.response.start",
                "status": 400,
                "headers": [(b"content-type", b"text/plain")],
            })
            await send({
                "type": "http.response.body",
                "body": b"Missing resource parameter",
                "more_body": False,
            })
            return
        match = re.match(
            r"^acct:([^@]+)@" + re.escape(context.request.host) + r"$",
            resource,
        )
        if not match:
            return await self.on_not_found(scope, receive, send)
        handle = match.group(1)
        actor = await self.server.dispatch_actor(context, handle)
        if actor is None:
            return await self.on_not_found(scope, receive, send)
        links: list[Link] = [
            Link(
                rel="self",
                href=context.actor_uri(handle),
                type=MediaType("application/activity+json"),
            )
        ]
        for url in actor.urls:
            if isinstance(url, link.Link):
                links.append(
                    Link(
                        rel=url.rel or "http://webfinger.net/rel/profile-page",
                        href=url.href,
                        type=(
                            None
                            if url.media_type is None
                            else MediaType(url.media_type)
                        ),
                    )
                )
            else:
                links.append(
                    Link(
                        rel="http://webfinger.net/rel/profile-page",
                        href=url,
                        type=MediaType("application/activity+json"),
                    )
                )
        jrd = ResourceDescriptor(
            subject=Uri(resource),
            aliases=[context.actor_uri(handle)],
            links=links,
        )
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"application/jrd+json")],
        })
        await send({
            "type": "http.response.body",
            "body": json.dumps(jrd.to_json()).encode("utf-8"),
            "more_body": False,
        })

    async def _actor_asgi(
        self,
        context: Context[TContextData],
        args: Mapping[str, Any],
        scope: Scope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ) -> None:
        actor: Optional[Actor] = await self.server.dispatch_actor(
            context, args["handle"]
        )
        if actor is None:
            return await self.on_not_found(scope, receive, send)
        doc = await jsonld(actor)
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [(
                b"content-type",
                (
                    b"application/ld+json;"
                    b' profile="https://www.w3.org/ns/activitystreams"'
                ),
            )],
        })
        await send({
            "type": "http.response.body",
            "body": json.dumps(doc).encode("utf-8"),
            "more_body": False,
        })

    async def _outbox_asgi(
        self,
        context: Context[TContextData],
        args: Mapping[str, Any],
        scope: Scope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ) -> None:
        handle = args["handle"]
        cursor = context.request.args.get("cursor")
        if cursor is None:
            first_cursor = await self.server.get_outbox_first_cursor(
                context, handle
            )
            last_cursor = await self.server.get_outbox_last_cursor(
                context, handle
            )
            total_items = await self.server.count_outbox(context, handle)
            if first_cursor is None:
                page: Optional[Page[Activity]] = (
                    await self.server.dispatch_outbox(
                        context, handle, cursor=None
                    )
                )
                if page is None:
                    return await self.on_not_found(scope, receive, send)
                _, _, items = page
                collection = OrderedCollection(
                    total_items=total_items,
                    ordered_items=items,
                )
            else:
                collection = OrderedCollection(
                    total_items=total_items,
                    first=EntityRef(
                        f"{context.outbox_uri(handle)}?cursor={quote(first_cursor)}"
                    ),
                    last=(
                        None
                        if last_cursor is None
                        else EntityRef(
                            f"{context.outbox_uri(handle)}?cursor={quote(last_cursor)}"
                        )
                    ),
                )
        else:
            page = await self.server.dispatch_outbox(context, handle, cursor)
            if page is None:
                return await self.on_not_found(scope, receive, send)
            prev_cursor, next_cursor, items = page
            collection = OrderedCollectionPage(
                prev=(
                    None
                    if prev_cursor is None
                    else EntityRef(
                        f"{context.outbox_uri(handle)}?cursor={quote(prev_cursor)}"
                    )
                ),
                next=(
                    None
                    if next_cursor is None
                    else EntityRef(
                        f"{context.outbox_uri(handle)}?cursor={quote(next_cursor)}"
                    )
                ),
                ordered_items=items,
            )
        doc = await jsonld(collection)
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [(
                b"content-type",
                (
                    b"application/ld+json;"
                    b' profile="https://www.w3.org/ns/activitystreams"'
                ),
            )],
        })
        await send({
            "type": "http.response.body",
            "body": json.dumps(doc).encode("utf-8"),
            "more_body": False,
        })
