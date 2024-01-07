import pytest

from fedikit.model.converters import from_jsonld, jsonld
from fedikit.model.docloader import DocumentLoader
from fedikit.model.entity import Uri
from fedikit.vocab.activity import Activity
from fedikit.vocab.actor import Person
from fedikit.vocab.link import Link
from fedikit.vocab.object import Object


@pytest.mark.parametrize("cls", [Object, Activity])
@pytest.mark.asyncio
async def test_activity_from_jsonld(
    cls: type[Object], document_loader: DocumentLoader
) -> None:
    parsed = await from_jsonld(
        cls,
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Activity",
            "attachment": [
                {"type": "Object", "name": "foo"},
                {"type": "Link", "as:href": "https://example.com/"},
            ],
            "object": [
                {"type": "Object", "name": "bar"},
                {"type": "Link", "as:href": "https://example.com/"},
            ],
        },
        loader=document_loader,
    )
    assert parsed == Activity(
        attachments=[
            Object(name="foo"),
            Link(href=Uri("https://example.com/")),
        ],
        objects=[
            Object(name="bar"),
            Link(href=Uri("https://example.com/")),
        ],
    )


@pytest.mark.asyncio
async def test_activity_attachment(document_loader: DocumentLoader) -> None:
    act = Activity(attachment=Object(name="foo"))
    assert act.attachment == Object(name="foo")
    assert act.attachments == [Object(name="foo")]
    assert await jsonld(act, expand=True, loader=document_loader) == {
        "@type": ["https://www.w3.org/ns/activitystreams#Activity"],
        "https://www.w3.org/ns/activitystreams#attachment": [
            {
                "@type": ["https://www.w3.org/ns/activitystreams#Object"],
                "https://www.w3.org/ns/activitystreams#name": [
                    {"@value": "foo"}
                ],
            },
        ],
    }
    assert await jsonld(act, loader=document_loader) == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Activity",
        "attachment": {"type": "Object", "name": "foo"},
    }


@pytest.mark.asyncio
async def test_activity_attributed_tos(
    document_loader: DocumentLoader,
) -> None:
    act = Activity(
        actors=[
            Person(name="foo"),
            Link(href=Uri("https://example.com/bar")),
        ],
        attributed_tos=[
            Person(name="baz"),
            Link(href=Uri("https://example.com/qux")),
        ],
    )
    assert act.actor == Person(name="foo")
    assert act.actors == [
        Person(name="foo"),
        Link(href=Uri("https://example.com/bar")),
    ]
    assert act.attributed_to == Person(name="baz")
    assert act.attributed_tos == [
        Person(name="baz"),
        Link(href=Uri("https://example.com/qux")),
        Person(name="foo"),
        Link(href=Uri("https://example.com/bar")),
    ]
    assert await jsonld(act, expand=True, loader=document_loader) == {
        "@type": ["https://www.w3.org/ns/activitystreams#Activity"],
        "https://www.w3.org/ns/activitystreams#actor": [
            {
                "@type": ["https://www.w3.org/ns/activitystreams#Person"],
                "https://www.w3.org/ns/activitystreams#name": [
                    {"@value": "foo"}
                ],
            },
            {
                "@type": ["https://www.w3.org/ns/activitystreams#Link"],
                "https://www.w3.org/ns/activitystreams#href": [
                    {"@value": "https://example.com/bar"}
                ],
            },
        ],
        "https://www.w3.org/ns/activitystreams#attributedTo": [
            {
                "@type": ["https://www.w3.org/ns/activitystreams#Person"],
                "https://www.w3.org/ns/activitystreams#name": [
                    {"@value": "baz"}
                ],
            },
            {
                "@type": ["https://www.w3.org/ns/activitystreams#Link"],
                "https://www.w3.org/ns/activitystreams#href": [
                    {"@value": "https://example.com/qux"}
                ],
            },
        ],
    }
    assert await jsonld(act, loader=document_loader) == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "actor": [
            {"name": "foo", "type": "Person"},
            {"as:href": "https://example.com/bar", "type": "Link"},
        ],
        "attributedTo": [
            {"name": "baz", "type": "Person"},
            {"as:href": "https://example.com/qux", "type": "Link"},
        ],
        "type": "Activity",
    }


@pytest.mark.asyncio
async def test_activity_object(document_loader: DocumentLoader) -> None:
    act = Activity(object=Object(name="foo"))
    assert act.object == Object(name="foo")
    assert act.objects == [Object(name="foo")]
    assert await jsonld(act, expand=True, loader=document_loader) == {
        "@type": ["https://www.w3.org/ns/activitystreams#Activity"],
        "https://www.w3.org/ns/activitystreams#object": [
            {
                "@type": ["https://www.w3.org/ns/activitystreams#Object"],
                "https://www.w3.org/ns/activitystreams#name": [
                    {"@value": "foo"}
                ],
            },
        ],
    }
    assert await jsonld(act, loader=document_loader) == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Activity",
        "object": {"type": "Object", "name": "foo"},
    }


@pytest.mark.asyncio
async def test_activity_objects(document_loader: DocumentLoader) -> None:
    act = Activity(
        objects=[
            Object(name="foo"),
            Link(href=Uri("https://example.com/")),
        ]
    )
    assert act.object == Object(name="foo")
    assert act.objects == [
        Object(name="foo"),
        Link(href=Uri("https://example.com/")),
    ]
    assert await jsonld(act, expand=True, loader=document_loader) == {
        "@type": ["https://www.w3.org/ns/activitystreams#Activity"],
        "https://www.w3.org/ns/activitystreams#object": [
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
    assert await jsonld(act, loader=document_loader) == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Activity",
        "object": [
            {"type": "Object", "name": "foo"},
            {"type": "Link", "as:href": "https://example.com/"},
        ],
    }
