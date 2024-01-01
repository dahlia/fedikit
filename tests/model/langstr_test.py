# cSpell: ignore Kore
import pytest
from langcodes import Language

from fedikit.model.converters import from_jsonld, jsonld
from fedikit.model.langstr import LanguageString


def test_language_string():
    ls = LanguageString("安寧, 世上아!", "ko-kore")
    assert str(ls) == "安寧, 世上아!"
    assert ls.language == Language.get("ko-Kore")
    assert repr(ls) == "LanguageString('安寧, 世上아!', language='ko-Kore')"


@pytest.mark.parametrize(
    "a, b",
    [
        (LanguageString("Hello", "en"), LanguageString("Hello", "en")),
        (LanguageString("Hello", "en"), LanguageString("Hello", "EN")),
    ],
)
def test_language_string_equality(
    a: LanguageString, b: LanguageString
) -> None:
    assert a == b
    assert b == a
    assert not (a != b)
    assert not (b != a)
    assert hash(a) == hash(b)


@pytest.mark.parametrize(
    "a, b",
    [
        (LanguageString("Hello", "en"), "Hello"),
        (LanguageString("安寧", "ko"), LanguageString("安寧", "ja")),
    ],
)
def test_language_string_inequality(a: str, b: str) -> None:
    assert not (a == b)
    assert not (b == a)
    assert a != b
    assert b != a
    assert hash(a) != hash(b)


@pytest.mark.asyncio
async def test_language_string_from_jsonld() -> None:
    assert await from_jsonld(
        LanguageString,
        {
            "@value": "Hello",
            "@language": "en",
        },
    ) == LanguageString("Hello", "en")


@pytest.mark.asyncio
async def test_language_string_jsonld():
    assert await jsonld(LanguageString("Hello", "en")) == {
        "@value": "Hello",
        "@language": "en",
    }
