from json import load
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from fedikit.model.docloader import RemoteDocument


def fixture_document_loader(url: str) -> Optional[RemoteDocument]:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return None
    doc_path = (
        Path(__file__).parent.parent
        / "fixtures"
        / parsed.netloc
        / parsed.path.lstrip("/")
    )
    if doc_path.is_file():
        with doc_path.open() as f:
            return RemoteDocument(
                content_type="application/ld+json",
                context_url=None,
                url=url,
                document=load(f),
            )
    return None
