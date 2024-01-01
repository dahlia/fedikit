import pytest

from fedikit.model.converters import from_jsonld, jsonld
from fedikit.model.docloader import DocumentLoader
from fedikit.model.entity import Uri
from fedikit.model.langstr import LanguageString
from fedikit.vocab.object import Object


@pytest.mark.asyncio
async def test_object_from_jsonld() -> None:
    parsed = await from_jsonld(
        Object,
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Object",
            "name": "foo",
        },
    )
    assert parsed == Object(name="foo")


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
