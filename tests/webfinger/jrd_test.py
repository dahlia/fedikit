from dataclasses import replace

from langcodes import Language

from fedikit.uri import Uri
from fedikit.webfinger.jrd import Link, MediaType, ResourceDescriptor


def test_resource_descriptor_to_json():
    rd = ResourceDescriptor(subject=Uri("acct:john@example.com"))
    assert rd.to_json() == {"subject": "acct:john@example.com"}
    rd = replace(
        rd,
        aliases=[Uri("https://example.com/")],
        properties={
            Uri("https://example.com/property"): "value",
        },
        links=[
            Link(
                rel=Uri("http://webfinger.net/rel/profile-page"),
                type=MediaType("text/html"),
                href=Uri("https://example.com/"),
                titles={
                    Language.get("en"): "Example",
                    Language.get("ko"): "예시",
                },
                properties={Uri("https://example.com/property"): "value"},
            ),
        ],
    )
    assert rd.to_json() == {
        "subject": "acct:john@example.com",
        "aliases": ["https://example.com/"],
        "properties": {
            "https://example.com/property": "value",
        },
        "links": [
            {
                "rel": "http://webfinger.net/rel/profile-page",
                "type": "text/html",
                "href": "https://example.com/",
                "titles": {
                    "en": "Example",
                    "ko": "예시",
                },
                "properties": {
                    "https://example.com/property": "value",
                },
            },
        ],
    }


def test_link_to_json():
    link = Link(rel=Uri("http://webfinger.net/rel/profile-page"))
    assert link.to_json() == {"rel": "http://webfinger.net/rel/profile-page"}
    link = replace(
        link,
        type=MediaType("text/html"),
        href=Uri("https://example.com/"),
        titles={Language.get("en"): "Example", Language.get("ko"): "예시"},
        properties={Uri("https://example.com/property"): "value"},
    )
    assert link.to_json() == {
        "rel": "http://webfinger.net/rel/profile-page",
        "type": "text/html",
        "href": "https://example.com/",
        "titles": {
            "en": "Example",
            "ko": "예시",
        },
        "properties": {
            "https://example.com/property": "value",
        },
    }
