from aiosqlite import Connection, connect
from quart import (
    Quart,
    ResponseReturnValue,
    current_app,
    redirect,
    render_template,
    request,
    url_for,
)

from .data import Metadata
from .db import add_post, get_metadata, get_posts, has_initialized, initialize
from .federation import CtxData, server

__all__ = ["app"]

app = Quart(__name__)
app.config.from_prefixed_env("FEDIBLOG")
app.asgi_app = server.asgi(  # type: ignore
    CtxData(app.config), app.asgi_app, app.asgi_app, app.asgi_app, app.asgi_app
)


def connect_db() -> Connection:
    return connect(current_app.config["DATABASE_PATH"])


@app.route("/")
async def index() -> ResponseReturnValue:
    async with connect_db() as db:
        if not await has_initialized(db):
            return redirect(url_for("setup"))
        metadata = await get_metadata(db)
        posts = [post async for post in get_posts(db)]
        return await render_template(
            "index.html", metadata=metadata, posts=posts
        )


@app.route("/posts/", methods=["POST"])
async def do_add_post() -> ResponseReturnValue:
    async with connect_db() as db:
        if not await has_initialized(db):
            return redirect(url_for("setup"))
        form = await request.form
        await add_post(db, form["content"])
        await db.commit()
        return redirect(url_for("index"), 303)


@app.route("/setup/")
async def setup() -> ResponseReturnValue:
    async with connect_db() as db:
        if await has_initialized(db):
            return redirect(url_for("index"))
        return await render_template("setup.html")


@app.route("/setup/", methods=["POST"])
async def do_setup() -> ResponseReturnValue:
    form = await request.form
    metadata = Metadata(
        handle=form["handle"],
        title=form["title"],
        description=form["description"],
    )
    async with connect_db() as db:
        if not await has_initialized(db):
            await initialize(db, metadata)
            await db.commit()
        return redirect(url_for("index"), 303)
