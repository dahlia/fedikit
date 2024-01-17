from collections.abc import AsyncIterable
from datetime import datetime
from typing import Optional, cast

from aiosqlite import Connection

from .data import Metadata, MetadataWithCreated, Post

__all__ = [
    "add_post",
    "count_posts",
    "get_metadata",
    "get_post",
    "get_posts",
    "has_initialized",
    "initialize",
]


async def has_initialized(db: Connection) -> bool:
    cursor = await db.execute("""
        SELECT count(*)
        FROM sqlite_schema
        WHERE type = 'table' AND name IN ('metadata', 'posts')
    """)
    async with cursor:
        row = await cursor.fetchone()
        return row is not None and row[0] == 2


async def initialize(db: Connection, metadata: Metadata) -> None:
    await db.execute("""
        CREATE TABLE metadata (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            handle TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    await db.execute("""
        CREATE TABLE posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            published TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    await db.execute(
        """
        INSERT INTO metadata (id, handle, title, description)
        VALUES (1, ?, ?, ?)
        """,
        (metadata.handle, metadata.title, metadata.description),
    )


async def get_metadata(db: Connection) -> MetadataWithCreated:
    cursor = await db.execute(
        "SELECT handle, title, description, created FROM metadata"
    )
    async with cursor:
        row = await cursor.fetchone()
        if row is None:
            raise RuntimeError("metadata not found")
        return MetadataWithCreated(
            row[0], row[1], row[2], datetime.fromisoformat(row[3] + "Z")
        )


async def add_post(db: Connection, content: str) -> None:
    await db.execute("INSERT INTO posts (content) VALUES (?)", (content,))


async def get_posts(
    db: Connection,
    offset: int = 0,
    limit: int = 5,
) -> AsyncIterable[Post]:
    cursor = await db.execute(
        """
        SELECT id, content, published FROM posts
        ORDER BY id DESC LIMIT ?, ?
        """,
        (offset, limit),
    )
    async with cursor:
        async for row in cursor:
            yield Post(row[0], row[1], datetime.fromisoformat(row[2] + "Z"))


async def get_post(db: Connection, post_id: int) -> Optional[Post]:
    cursor = await db.execute(
        "SELECT content, published FROM posts WHERE id = ?",
        (post_id,),
    )
    async with cursor:
        async for row in cursor:
            return Post(post_id, row[0], datetime.fromisoformat(row[1] + "Z"))
    return None


async def count_posts(db: Connection) -> int:
    cursor = await db.execute("SELECT count(*) FROM posts")
    async with cursor:
        row = await cursor.fetchone()
        return 0 if row is None else cast(int, row[0])
