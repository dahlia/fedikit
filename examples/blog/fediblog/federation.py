from collections.abc import Mapping
from dataclasses import dataclass
from html import escape
from typing import Any, Final, Optional

from aiosqlite import Connection, connect
from fedikit.federation.collection import Page
from fedikit.federation.server import Context, Request, Server
from fedikit.model.entity import EntityRef
from fedikit.uri import Uri
from fedikit.vocab import Activity, Actor, Create, Note, Person
from quart import Quart
from quart import Request as QRequest

from .db import count_posts, get_metadata, get_posts

__all__ = ["CtxData", "server"]


@dataclass(frozen=True)
class CtxData:
    app: Quart

    @property
    def config(self) -> Mapping[str, Any]:
        return self.app.config

    async def url_for(self, request: Request, name: str, **kwargs: Any) -> Uri:
        async def void(_: Any, __: Any) -> None:
            return None

        qr = QRequest(
            request.method,
            request.scheme,
            request.path,
            request.query_string,
            request.headers,
            request.root_path,
            "1.1",
            {"type": "http"},  # type: ignore
            send_push_promise=void,
        )
        async with self.app.request_context(qr):
            return Uri(self.app.url_for(name, **kwargs, _external=True))

    def connect_db(self) -> Connection:
        return connect(self.config["DATABASE_PATH"])


server = Server[CtxData]()


@server.actor_dispatcher("/actors/<handle>/")
async def dispatch_actor(
    context: Context[CtxData], handle: str
) -> Optional[Actor]:
    async with context.data.connect_db() as db:
        metadata = await get_metadata(db)
        if metadata.handle != handle:
            return None
        return Person(
            id=context.actor_uri(handle),
            preferred_username=metadata.handle,
            name=metadata.title,
            summary=f"<p>{escape(metadata.description)}</p>",
            published=metadata.created,
            outbox=EntityRef(context.outbox_uri(handle)),
        )


PAGE_WINDOW: Final[int] = 5


@server.outbox_dispatcher("/actors/<handle>/outbox/")
async def dispatch_outbox(
    context: Context[CtxData], handle: str, cursor: Optional[str]
) -> Optional[Page[Activity]]:
    if cursor is None:
        return None
    offset = int(cursor)
    async with context.data.connect_db() as db:
        metadata = await get_metadata(db)
        if metadata.handle != handle:
            return None
        activities: list[Activity] = []
        async for post in get_posts(db, offset=offset, limit=PAGE_WINDOW):
            activity = Create(
                actor=EntityRef(context.actor_uri(handle)),
                object=Note(
                    content=post.content,
                    published=post.published,
                    url=await context.data.url_for(
                        context.request, "show_post", post_id=post.id
                    ),
                ),
            )
            activities.append(activity)
        total = await count_posts(db)
        return Page(
            prev_cursor=(
                None
                if offset < 1
                else str(offset - PAGE_WINDOW if offset > PAGE_WINDOW else 0)
            ),
            next_cursor=(
                str(offset + PAGE_WINDOW)
                if offset + PAGE_WINDOW < total
                else None
            ),
            items=activities,
        )


@server.outbox_counter
async def count_outbox(context: Context[CtxData], handle: str) -> int:
    async with context.data.connect_db() as db:
        return await count_posts(db)


@server.outbox_first_cursor
async def first_outbox_cursor(context: Context[CtxData], handle: str) -> str:
    return "0"


@server.outbox_last_cursor
async def last_outbox_cursor(context: Context[CtxData], handle: str) -> str:
    async with context.data.connect_db() as db:
        return str((await count_posts(db) // PAGE_WINDOW) * PAGE_WINDOW)
