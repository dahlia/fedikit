import pytest
from cryptography.hazmat.primitives.serialization import load_ssh_public_key

from fedikit.model.converters import from_jsonld, jsonld
from fedikit.model.docloader import DocumentLoader
from fedikit.model.entity import EntityRef
from fedikit.uri import Uri
from fedikit.vocab.actor import Actor, Key, Person


@pytest.mark.asyncio
async def test_actor_from_jsonld(document_loader: DocumentLoader) -> None:
    parsed = await from_jsonld(
        Actor,
        {
            "@context": [
                "https://www.w3.org/ns/activitystreams",
                "https://w3id.org/security/v1",
            ],
            "id": "https://example.com/john",
            "type": "Person",
            "publicKey": {
                "id": "https://example.com/john#main-key",
                "owner": "https://example.com/john",
                "publicKeyPem": (
                    "-----BEGIN PUBLIC KEY-----\n"
                    + "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4UUGGbEGtalj2r+ZAVKU\n"
                    + "c4o8yrgknzdXqj7lk4fhLuG/DpSOWrTUfNofEHSHympufcXtJdWtfLvJYAY19r7x\n"
                    + "uUziR1F7r2RxFD+nz6gjyI+cvbx9wWNfLeJHckRv9g0tDvYkXr9BOhC9L/r6s4Ir\n"
                    + "yx6qaUhw36vrbRD/IHSyn4IU6LwX+vVSi98/3aupRczU9m3p9EOwSYuFQfSb4iYU\n"
                    + "3AB984QCFRONak/WEjVof4g6qWBxoZGvCu2rQJkT4KA9smmoVO+iLAHH6JSP3zYi\n"
                    + "xqv2wRMNPrPIUzMpW3jf9M3jU+PUf/AupVc+UW/WdiA8wCVcYL3YVYLNkR9BI89x\n"
                    + "vwIDAQAB\n"
                    + "-----END PUBLIC KEY-----\n"
                ),
            },
        },
    )
    assert parsed == Person(
        id=Uri("https://example.com/john"),
        public_key=Key(
            id=Uri("https://example.com/john#main-key"),
            owner=EntityRef("https://example.com/john"),
            public_key=load_ssh_public_key(
                b"ssh-rsa"
                b" AAAAB3NzaC1yc2EAAAADAQABAAABAQDhRQYZsQa1qWPav5kBUpRzijzKuCSfN1eqPuWTh+Eu4b8OlI5atNR82h8QdIfKam59xe0l1a18u8lgBjX2vvG5TOJHUXuvZHEUP6fPqCPIj5y9vH3BY18t4kdyRG/2DS0O9iRev0E6EL0v+vqzgivLHqppSHDfq+ttEP8gdLKfghTovBf69VKL3z/dq6lFzNT2ben0Q7BJi4VB9JviJhTcAH3zhAIVE41qT9YSNWh/iDqpYHGhka8K7atAmRPgoD2yaahU76IsAcfolI/fNiLGq/bBEw0+s8hTMylbeN/0zeNT49R/8C6lVz5Rb9Z2IDzAJVxgvdhVgs2RH0Ejz3G/"
            ),
        ),
    )


@pytest.mark.asyncio
async def test_actor_public_key(document_loader: DocumentLoader) -> None:
    actor = Person(
        id=Uri("https://example.com/john"),
        public_key=Key(
            id=Uri("https://example.com/john#main-key"),
            owner=EntityRef("https://example.com/john"),
            public_key=load_ssh_public_key(
                b"ssh-rsa"
                b" AAAAB3NzaC1yc2EAAAADAQABAAABAQDhRQYZsQa1qWPav5kBUpRzijzKuCSfN1eqPuWTh+Eu4b8OlI5atNR82h8QdIfKam59xe0l1a18u8lgBjX2vvG5TOJHUXuvZHEUP6fPqCPIj5y9vH3BY18t4kdyRG/2DS0O9iRev0E6EL0v+vqzgivLHqppSHDfq+ttEP8gdLKfghTovBf69VKL3z/dq6lFzNT2ben0Q7BJi4VB9JviJhTcAH3zhAIVE41qT9YSNWh/iDqpYHGhka8K7atAmRPgoD2yaahU76IsAcfolI/fNiLGq/bBEw0+s8hTMylbeN/0zeNT49R/8C6lVz5Rb9Z2IDzAJVxgvdhVgs2RH0Ejz3G/"
            ),
        ),
    )
    assert actor.public_key == Key(
        id=Uri("https://example.com/john#main-key"),
        owner=EntityRef("https://example.com/john"),
        public_key=load_ssh_public_key(
            b"ssh-rsa"
            b" AAAAB3NzaC1yc2EAAAADAQABAAABAQDhRQYZsQa1qWPav5kBUpRzijzKuCSfN1eqPuWTh+Eu4b8OlI5atNR82h8QdIfKam59xe0l1a18u8lgBjX2vvG5TOJHUXuvZHEUP6fPqCPIj5y9vH3BY18t4kdyRG/2DS0O9iRev0E6EL0v+vqzgivLHqppSHDfq+ttEP8gdLKfghTovBf69VKL3z/dq6lFzNT2ben0Q7BJi4VB9JviJhTcAH3zhAIVE41qT9YSNWh/iDqpYHGhka8K7atAmRPgoD2yaahU76IsAcfolI/fNiLGq/bBEw0+s8hTMylbeN/0zeNT49R/8C6lVz5Rb9Z2IDzAJVxgvdhVgs2RH0Ejz3G/"
        ),
    )
    assert await jsonld(actor, loader=document_loader) == {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://w3id.org/security/v1",
        ],
        "id": "https://example.com/john",
        "type": "Person",
        "publicKey": {
            "id": "https://example.com/john#main-key",
            "type": "CryptographicKey",
            "owner": "https://example.com/john",
            "publicKeyPem": (
                "-----BEGIN PUBLIC KEY-----\n"
                + "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4UUGGbEGtalj2r+ZAVKU\n"
                + "c4o8yrgknzdXqj7lk4fhLuG/DpSOWrTUfNofEHSHympufcXtJdWtfLvJYAY19r7x\n"
                + "uUziR1F7r2RxFD+nz6gjyI+cvbx9wWNfLeJHckRv9g0tDvYkXr9BOhC9L/r6s4Ir\n"
                + "yx6qaUhw36vrbRD/IHSyn4IU6LwX+vVSi98/3aupRczU9m3p9EOwSYuFQfSb4iYU\n"
                + "3AB984QCFRONak/WEjVof4g6qWBxoZGvCu2rQJkT4KA9smmoVO+iLAHH6JSP3zYi\n"
                + "xqv2wRMNPrPIUzMpW3jf9M3jU+PUf/AupVc+UW/WdiA8wCVcYL3YVYLNkR9BI89x\n"
                + "vwIDAQAB\n"
                + "-----END PUBLIC KEY-----\n"
            ),
        },
    }


# cSpell: ignore IDAQAB
