import pytest

from fedikit.model.docloader import DocumentLoader

from .model.docloader import fixture_document_loader


@pytest.fixture
def document_loader() -> DocumentLoader:
    return fixture_document_loader
