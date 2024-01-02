import pytest
from langcodes import Language

from fedikit.model.converters import from_jsonld, jsonld
from fedikit.model.docloader import DocumentLoader
from fedikit.model.entity import Uri
from fedikit.vocab.link import Link


@pytest.mark.asyncio
async def test_object_from_jsonld() -> None:
    parsed = await from_jsonld(
        Link,
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Link",
            "as:href": "https://example.com/",
            "hreflang": "en",
        },
    )
    assert parsed == Link(
        href=Uri("https://example.com/"), hreflang=Language.get("en")
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
