from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Optional, cast

import pytest
from asgi_tools.tests import ASGITestClient
from asgi_tools.types import TASGIApp
from fedikit.federation.server import Context, Server
from fedikit.uri import Uri
from fedikit.vocab.actor import Actor, Person

actors: dict[str, Callable[[Uri], Actor]] = {
    "alice": lambda uri: Person(
        id=uri,
        preferred_username="alice",
        name="Alice",
        summary="<p>Alice's summary</p>",
        published=datetime(2021, 1, 1),
    ),
    "bob": lambda uri: Person(
        id=uri,
        preferred_username="bob",
        name="Bob",
        summary="<p>Bob's summary</p>",
        published=datetime(2022, 1, 1),
    ),
}


@dataclass(frozen=True)
class CtxData:
    actors: Mapping[str, Callable[[Uri], Actor]]


server: Server[CtxData] = Server[CtxData]()


@server.actor_dispatcher("/actors/<handle>")
async def dispatch_actor(
    context: Context[CtxData], handle: str
) -> Optional[Actor]:
    if handle not in context.data.actors:
        return None
    return context.data.actors[handle](context.actor_uri(handle))


@pytest.fixture
def client() -> ASGITestClient:
    asgi_app = cast(TASGIApp, server.asgi(CtxData(actors)))
    client = ASGITestClient(asgi_app, "http://fedikit.test")
    client.headers = {
        "Host": "fedikit.test",
    }
    return client


@pytest.mark.asyncio
async def test_webfinger(client: ASGITestClient) -> None:
    alice = await client.request(
        "/.well-known/webfinger?resource=acct:alice@fedikit.test",
        "GET",
    )
    assert alice.status_code == 200
    assert alice.content_type == "application/jrd+json"
    assert await alice.json() == {
        "subject": "acct:alice@fedikit.test",
        "aliases": ["http://fedikit.test/actors/alice"],
        "links": [{
            "rel": "self",
            "type": "application/activity+json",
            "href": "http://fedikit.test/actors/alice",
        }],
    }

    bob = await client.request(
        "/.well-known/webfinger?resource=acct:bob@fedikit.test",
        "GET",
    )
    assert bob.status_code == 200
    assert bob.content_type == "application/jrd+json"
    assert await bob.json() == {
        "subject": "acct:bob@fedikit.test",
        "aliases": ["http://fedikit.test/actors/bob"],
        "links": [{
            "rel": "self",
            "type": "application/activity+json",
            "href": "http://fedikit.test/actors/bob",
        }],
    }

    non_existent = await client.request(
        "/.well-known/webfinger?resource=acct:non-existent@fedikit.test",
        "GET",
    )
    assert non_existent.status_code == 404

    other_host = await client.request(
        "/.well-known/webfinger?resource=acct:alice@other.host",
        "GET",
    )
    assert other_host.status_code == 404

    non_acct = await client.request(
        "/.well-known/webfinger?resource=http://fedikit.test/actors/alice",
        "GET",
    )
    assert non_acct.status_code == 404


@pytest.mark.asyncio
async def test_actor_dispatcher(client: ASGITestClient) -> None:
    alice = await client.request("/actors/alice", "GET")
    assert alice.status_code == 200
    assert alice.content_type == "application/ld+json"
    assert await alice.json() == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": "http://fedikit.test/actors/alice",
        "type": "Person",
        "preferredUsername": "alice",
        "name": "Alice",
        "summary": "<p>Alice's summary</p>",
        "published": "2021-01-01T00:00:00",
    }

    bob = await client.request("/actors/bob", "GET")
    assert bob.status_code == 200
    assert bob.content_type == "application/ld+json"
    assert await bob.json() == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": "http://fedikit.test/actors/bob",
        "type": "Person",
        "preferredUsername": "bob",
        "name": "Bob",
        "summary": "<p>Bob's summary</p>",
        "published": "2022-01-01T00:00:00",
    }

    non_existent = await client.request("/actors/non-existent", "GET")
    assert non_existent.status_code == 404


# cSpell: ignore TASGI