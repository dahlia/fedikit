from decimal import Decimal

import pytest
from isoduration.types import DateDuration, Duration, TimeDuration

from fedikit.model.converters import from_jsonld, jsonld
from fedikit.model.docloader import DocumentLoader
from fedikit.model.entity import EntityRef, Uri
from fedikit.model.langstr import LanguageString
from fedikit.vocab.collection import Collection
from fedikit.vocab.link import Link
from fedikit.vocab.object import Object, Place


@pytest.mark.asyncio
async def test_object_from_jsonld() -> None:
    parsed = await from_jsonld(
        Object,
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Object",
            "name": "foo",
            "attachment": [
                {"type": "Object", "name": "foo"},
                {"type": "Link", "as:href": "https://example.com/"},
            ],
            "duration": "P1DT2H",
            "replies": {
                "type": "Collection",
                "totalItems": 1,
                "items": [{"name": "reply", "type": "Object"}],
            },
        },
    )
    assert parsed == Object(
        name="foo",
        attachments=[
            Object(name="foo"),
            Link(href=Uri("https://example.com/")),
        ],
        duration=Duration(
            DateDuration(days=Decimal(1)), TimeDuration(hours=Decimal(2))
        ),
        replies=Collection(
            total_items=1,
            items=[Object(name="reply")],
        ),
    )

    # Entity refs can be used as property values (nodes that have only @id):
    parsed2 = await from_jsonld(
        Object,
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Object",
            "name": "foo",
            "attachment": [
                "https://example.com/foo",
                {"type": "Link", "as:href": "https://example.com/"},
            ],
        },
    )
    assert isinstance(parsed2, Object)
    assert parsed2.name == "foo"
    assert parsed2.attachments == [Link(href=Uri("https://example.com/"))]


@pytest.mark.asyncio
async def test_object_attachment(document_loader: DocumentLoader) -> None:
    obj = Object(attachment=Object(name="foo"))
    assert obj.attachment == Object(name="foo")
    assert obj.attachments == [Object(name="foo")]
    assert await jsonld(obj, expand=True, loader=document_loader) == {
        "@type": ["https://www.w3.org/ns/activitystreams#Object"],
        "https://www.w3.org/ns/activitystreams#attachment": [
            {
                "@type": ["https://www.w3.org/ns/activitystreams#Object"],
                "https://www.w3.org/ns/activitystreams#name": [
                    {"@value": "foo"}
                ],
            },
        ],
    }
    assert await jsonld(obj, loader=document_loader) == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Object",
        "attachment": {"type": "Object", "name": "foo"},
    }


@pytest.mark.asyncio
async def test_object_attachments(document_loader: DocumentLoader) -> None:
    obj = Object(
        attachments=[
            Object(name="foo"),
            Link(href=Uri("https://example.com/")),
        ]
    )
    assert obj.attachment == Object(name="foo")
    assert obj.attachments == [
        Object(name="foo"),
        Link(href=Uri("https://example.com/")),
    ]
    assert await jsonld(obj, expand=True, loader=document_loader) == {
        "@type": ["https://www.w3.org/ns/activitystreams#Object"],
        "https://www.w3.org/ns/activitystreams#attachment": [
            {
                "@type": ["https://www.w3.org/ns/activitystreams#Object"],
                "https://www.w3.org/ns/activitystreams#name": [
                    {"@value": "foo"}
                ],
            },
            {
                "@type": ["https://www.w3.org/ns/activitystreams#Link"],
                "https://www.w3.org/ns/activitystreams#href": [
                    {"@value": "https://example.com/"},
                ],
            },
        ],
    }
    assert await jsonld(obj, loader=document_loader) == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Object",
        "attachment": [
            {"type": "Object", "name": "foo"},
            {"type": "Link", "as:href": "https://example.com/"},
        ],
    }


@pytest.mark.asyncio
async def test_object_name(document_loader: DocumentLoader) -> None:
    obj = Object(id=Uri("https://example.com/object"), name="foo")
    assert obj.name == "foo"
    assert obj.names == ["foo"]
    assert await jsonld(obj, expand=True, loader=document_loader) == {
        "@type": ["https://www.w3.org/ns/activitystreams#Object"],
        "@id": "https://example.com/object",
        "https://www.w3.org/ns/activitystreams#name": [{"@value": "foo"}],
    }
    assert await jsonld(obj, loader=document_loader) == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": "https://example.com/object",
        "type": "Object",
        "name": "foo",
    }

    obj2 = Object(name=LanguageString("你好", "zh"))
    assert obj2.name == LanguageString("你好", "zh")
    assert obj2.names == [LanguageString("你好", "zh")]
    assert await jsonld(obj2, expand=True, loader=document_loader) == {
        "@type": ["https://www.w3.org/ns/activitystreams#Object"],
        "https://www.w3.org/ns/activitystreams#name": [
            {"@value": "你好", "@language": "zh"}
        ],
    }
    assert await jsonld(obj2, loader=document_loader) == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Object",
        "nameMap": {"zh": "你好"},
    }


@pytest.mark.asyncio
async def test_object_names(document_loader: DocumentLoader) -> None:
    obj = Object(names=["foo", "bar"])
    assert obj.name == "foo"
    assert obj.names == ["foo", "bar"]
    assert await jsonld(obj, loader=document_loader) == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Object",
        "name": ["foo", "bar"],
    }

    obj2 = Object(
        names=[
            LanguageString("你好", "zh"),
            LanguageString("Hello", "en"),
        ]
    )
    assert obj2.name == LanguageString("你好", "zh")
    assert obj2.names == [
        LanguageString("你好", "zh"),
        LanguageString("Hello", "en"),
    ]
    assert await jsonld(obj2, loader=document_loader) == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Object",
        "nameMap": {"zh": "你好", "en": "Hello"},
    }


@pytest.mark.asyncio
async def test_object_duration(document_loader: DocumentLoader) -> None:
    duration = Duration(
        DateDuration(days=Decimal(1)), TimeDuration(hours=Decimal(2))
    )
    obj = Object(duration=duration)
    assert obj.duration == duration
    assert await jsonld(obj, loader=document_loader) == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Object",
        "as:duration": "P1DT2H",
    }


@pytest.mark.parametrize(
    "a, b",
    [
        (Object(name="foo"), Object(name="foo")),
        (Object(name="foo"), Object(names=["foo"])),
        (Object(names=["foo", "bar"]), Object(names=["foo", "bar"])),
    ],
)
def test_object_equality(a: Object, b: Object) -> None:
    assert a == b
    assert b == a
    assert not (a != b)
    assert not (b != a)
    assert hash(a) == hash(b)


@pytest.mark.parametrize(
    "a, b",
    [
        (Object(name="foo"), Object(name="bar")),
        (Object(name="foo"), Object(names=["bar"])),
        (Object(name="foo"), Object(names=["foo", "bar"])),
        (Object(names=["foo", "bar"]), Object(names=["bar", "foo"])),
        (Object(names=["foo", "bar"]), Object(names=["foo", "bar", "baz"])),
    ],
)
def test_object_inequality(a: Object, b: Object) -> None:
    assert a != b
    assert b != a
    assert not (a == b)
    assert not (b == a)
    assert hash(a) != hash(b)


def test_object_repr():
    assert repr(Object(name="foo")) == "Object(name='foo')"
    assert repr(Object(names=["foo", "bar"])) == "Object(names=['foo', 'bar'])"
    assert (
        repr(
            Object(
                names=["foo", "bar"],
                attachments=[
                    EntityRef("https://example.com/"),  # type: ignore
                    Object(name="baz"),
                ],
            )
        )
        == "Object(names=['foo', 'bar'], "
        "attachments=[EntityRef('https://example.com/'), Object(name='baz')])"
    )
    assert (
        repr(
            Object(
                names=["foo", "bar"],
                __extra__={  # type: ignore
                    "https://example.com/": {"@value": "foo"},
                },
            )
        )
        == "Object(names=['foo', 'bar'], "
        "__extra__={'https://example.com/': {'@value': 'foo'}})"
    )


@pytest.mark.asyncio
async def test_place_from_jsonld() -> None:
    parsed = await from_jsonld(
        Object,
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Place",
            "latitude": 35.1483528,
            "longitude": 126.9161773,
            "units": "miles",
        },
    )
    assert parsed == Place(
        latitude=35.1483528, longitude=126.9161773, units="miles"
    )


@pytest.mark.asyncio
async def test_place_properties(document_loader: DocumentLoader) -> None:
    place = Place(latitude=35.1483528, longitude=126.9161773, units="cm")
    assert place.units == "cm"
    assert await jsonld(place, loader=document_loader) == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Place",
        "latitude": 35.1483528,
        "longitude": 126.9161773,
        "units": "cm",
    }
