from typing import Any

import pytest

from fedikit.model.docloader import DocumentLoader
from fedikit.model.entity import Entity, EntityRef, Uri, load_entity_refs
from fedikit.vocab.link import Link
from fedikit.vocab.object import Object


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
    obj = Object(
        attachment=EntityRef("https://example.com/foo"),  # type: ignore
    )
    assert obj.attachment is None
    await load_entity_refs(obj, loader=document_loader)
    assert obj.attachment == Object(
        name="foo",
        attachments=[
            Object(name="bar"),
            Link(href=Uri("https://example.com/")),
        ],
    )
