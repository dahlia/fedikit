from typing import Any

import pytest

from fedikit.model.docloader import DocumentLoader
from fedikit.model.entity import Entity, EntityRef, load_entity_refs
from fedikit.uri import Uri
from fedikit.vocab.activity import Activity
from fedikit.vocab.document import Page
from fedikit.vocab.link import Link
from fedikit.vocab.object import Object


@pytest.mark.asyncio
async def test_entity_from_jsonld(document_loader: DocumentLoader) -> None:
    page = await Entity.__from_jsonld__(
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Page",
            "name": "foo",
        },
        loader=document_loader,
    )
    assert isinstance(page, Page)
    assert page == Page(name="foo")


def test_entity_ref_uri():
    assert EntityRef("https://example.com/").uri == Uri("https://example.com/")


@pytest.mark.parametrize(
    "a, b",
    [
        (
            EntityRef("https://example.com/"),
            EntityRef(Uri("https://example.com/")),
        ),
        (EntityRef("https://example.com/"), EntityRef("https://example.com/")),
    ],
)
def test_entity_ref_equality(a: EntityRef, b: EntityRef) -> None:
    assert a == b
    assert b == a
    assert not (a != b)
    assert not (b != a)
    assert hash(a) == hash(b)


@pytest.mark.parametrize(
    "a, b",
    [
        (
            EntityRef("https://example.com/foo"),
            EntityRef(Uri("https://example.com/bar")),
        ),
        (
            EntityRef("https://example.com/foo"),
            EntityRef("https://example.com/bar"),
        ),
    ],
)
def test_entity_ref_inequality(a: EntityRef, b: Any) -> None:
    assert a != b
    assert b != a
    assert not (a == b)
    assert not (b == a)
    assert hash(a) != hash(b)


@pytest.mark.asyncio
async def test_entity_ref_load(document_loader: DocumentLoader) -> None:
    ref = EntityRef("https://example.com/foo")
    entity = await ref.load(Entity, loader=document_loader)
    assert entity == Object(
        name="foo",
        attachments=[
            Object(name="bar"),
            Link(href=Uri("https://example.com/")),
        ],
    )


@pytest.mark.asyncio
async def test_load_entity_refs(document_loader: DocumentLoader) -> None:
    act = Activity(
        attachment=EntityRef("https://example.com/foo"),  # type: ignore
        object=EntityRef("https://example.com/bar"),  # type: ignore
    )
    assert act.attachment is None
    assert act.object is None
    await load_entity_refs(act, "attachment", loader=document_loader)
    assert act.attachment == Object(
        name="foo",
        attachments=[
            Object(name="bar"),
            Link(href=Uri("https://example.com/")),
        ],
    )
    assert act.object is None

    act2 = Activity(
        attachment=EntityRef("https://example.com/foo"),  # pyright: ignore
        object=EntityRef("https://example.com/bar"),  # pyright: ignore
    )
    assert act2.attachment is None
    assert act2.object is None
    await load_entity_refs(act2, loader=document_loader)
    assert act2.attachment == Object(
        name="foo",
        attachments=[
            Object(name="bar"),
            Link(href=Uri("https://example.com/")),
        ],
    )
    assert act2.object == Object(name="bar")
