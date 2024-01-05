from typing import Any

import pytest

from fedikit.model.entity import EntityRef, Uri


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
