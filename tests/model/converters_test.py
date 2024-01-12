from datetime import UTC, datetime

import pytest
from langcodes import Language

from fedikit.model.converters import from_jsonld, jsonld
from fedikit.uri import Uri


@pytest.mark.asyncio
async def test_str_jsonld():
    assert await jsonld("Hello") == {"@value": "Hello"}


@pytest.mark.asyncio
async def test_bool_jsonld():
    assert await jsonld(True) == {"@value": True}
    assert await jsonld(False) == {"@value": False}


@pytest.mark.asyncio
async def test_int_jsonld():
    assert await jsonld(42) == {
        "@value": 42,
        "@type": "http://www.w3.org/2001/XMLSchema#nonNegativeInteger",
    }
    assert await jsonld(-42) == {
        "@value": -42,
        "@type": "http://www.w3.org/2001/XMLSchema#integer",
    }


@pytest.mark.asyncio
async def test_datetime_jsonld():
    assert await jsonld(datetime(2024, 1, 2, 3, 4, 5, 6, UTC)) == {
        "@type": "http://www.w3.org/2001/XMLSchema#dateTime",
        "@value": "2024-01-02T03:04:05.000006+00:00",
    }


@pytest.mark.asyncio
async def test_uri_jsonld():
    assert await jsonld(Uri("https://example.com/")) == {
        "@value": "https://example.com/"
    }


@pytest.mark.asyncio
async def test_language_jsonld():
    assert await jsonld(Language.get("KO-KR")) == {"@value": "ko-KR"}


@pytest.mark.asyncio
async def test_str_from_jsonld():
    assert await from_jsonld(str, {"@value": "Hello"}) == "Hello"


@pytest.mark.asyncio
async def test_bool_from_jsonld():
    assert await from_jsonld(bool, {"@value": True}) is True
    assert await from_jsonld(bool, {"@value": False}) is False


@pytest.mark.asyncio
async def test_int_from_jsonld():
    assert (
        await from_jsonld(
            int,
            {
                "@value": 42,
                "@type": "http://www.w3.org/2001/XMLSchema#nonNegativeInteger",
            },
        )
        == 42
    )
    assert (
        await from_jsonld(
            int,
            {
                "@value": -42,
                "@type": "http://www.w3.org/2001/XMLSchema#integer",
            },
        )
        == -42
    )


@pytest.mark.asyncio
async def test_datetime_from_jsonld():
    assert await from_jsonld(
        datetime,
        {
            "@type": "http://www.w3.org/2001/XMLSchema#dateTime",
            "@value": "2024-01-02T03:04:05.000006+00:00",
        },
    ) == datetime(2024, 1, 2, 3, 4, 5, 6, UTC)


@pytest.mark.asyncio
async def test_uri_from_jsonld():
    assert await from_jsonld(Uri, {"@value": "https://example.com/"}) == Uri(
        "https://example.com/"
    )


@pytest.mark.asyncio
async def test_language_from_jsonld():
    assert await from_jsonld(Language, {"@value": "ko-KR"}) == Language.get(
        "ko-KR"
    )
