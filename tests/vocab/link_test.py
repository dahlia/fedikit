import pytest
from langcodes import Language

from fedikit.model.converters import from_jsonld, jsonld
from fedikit.model.docloader import DocumentLoader
from fedikit.model.entity import Uri
from fedikit.vocab.link import Link
from fedikit.vocab.object import Object


@pytest.mark.asyncio
async def test_object_from_jsonld() -> None:
    parsed = await from_jsonld(
        Link,
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Link",
            "as:href": "https://example.com/",
            "hreflang": "en",
            "width": 200,
            "height": 150,
            "preview": [
                {"type": "Object", "name": "foo"},
                {"type": "Link", "as:href": "https://example.com/preview"},
            ],
        },
    )
    assert parsed == Link(
        href=Uri("https://example.com/"),
        hreflang=Language.get("en"),
        width=200,
        height=150,
        previews=[
            Object(name="foo"),
            Link(href=Uri("https://example.com/preview")),
        ],
    )


@pytest.mark.asyncio
async def test_link_href(document_loader: DocumentLoader) -> None:
    link = Link(href=Uri("https://example.com/"))
    assert link.href == Uri("https://example.com/")
    assert await jsonld(link, expand=True, loader=document_loader) == {
        "@type": ["https://www.w3.org/ns/activitystreams#Link"],
        "https://www.w3.org/ns/activitystreams#href": [
            {"@value": "https://example.com/"},
        ],
    }
    assert await jsonld(link, loader=document_loader) == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Link",
        "as:href": "https://example.com/",
    }


@pytest.mark.asyncio
async def test_link_hreflang(document_loader: DocumentLoader) -> None:
    link = Link(href=Uri("https://example.com/"), hreflang=Language.get("en"))
    assert link.hreflang == Language.get("en")
    assert await jsonld(link, expand=True, loader=document_loader) == {
        "@type": ["https://www.w3.org/ns/activitystreams#Link"],
        "https://www.w3.org/ns/activitystreams#href": [
            {"@value": "https://example.com/"},
        ],
        "https://www.w3.org/ns/activitystreams#hreflang": [
            {"@value": "en"},
        ],
    }
    assert await jsonld(link, loader=document_loader) == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Link",
        "as:href": "https://example.com/",
        "hreflang": "en",
    }


@pytest.mark.asyncio
async def test_link_width_height(document_loader: DocumentLoader) -> None:
    link = Link(href=Uri("https://example.com/a.png"), width=200, height=150)
    assert link.href == Uri("https://example.com/a.png")
    assert link.width == 200
    assert link.height == 150
    assert await jsonld(link, expand=True, loader=document_loader) == {
        "@type": ["https://www.w3.org/ns/activitystreams#Link"],
        "https://www.w3.org/ns/activitystreams#href": [
            {"@value": "https://example.com/a.png"},
        ],
        "https://www.w3.org/ns/activitystreams#width": [
            {
                "@type": "http://www.w3.org/2001/XMLSchema#nonNegativeInteger",
                "@value": 200,
            },
        ],
        "https://www.w3.org/ns/activitystreams#height": [
            {
                "@type": "http://www.w3.org/2001/XMLSchema#nonNegativeInteger",
                "@value": 150,
            },
        ],
    }
    assert await jsonld(link, loader=document_loader) == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Link",
        "as:href": "https://example.com/a.png",
        "width": 200,
        "height": 150,
    }
