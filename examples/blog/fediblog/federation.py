from collections.abc import Mapping
from dataclasses import dataclass
from html import escape
from typing import Any, Optional

from aiosqlite import Connection, connect
from fedikit.federation.server import Context, Server
from fedikit.vocab import Actor, Person

from .db import get_metadata

__all__ = ["CtxData", "server"]


@dataclass(frozen=True)
class CtxData:
    config: Mapping[str, Any]

    def connect_db(self) -> Connection:
        return connect(self.config["DATABASE_PATH"])


server = Server[CtxData]()


@server.actor_dispatcher("/actors/<handle>")
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
        )
