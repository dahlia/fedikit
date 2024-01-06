from typing import Any, Mapping, Optional, Self

from langcodes import Language

from .docloader import DocumentLoader

__all__ = ["LanguageString"]


class LanguageString(str):
    """A string with an associated language tag.  This is used to represent
    a ``rdf:langString`` value, a language-tagged string in the Activity
    Vocabulary.
    """

    #: The language tag associated with the string.
    language: Language

    def __new__(cls, value: str, language: Language | str) -> Self:
        return super().__new__(cls, value)

    def __init__(self, value: str, language: Language | str) -> None:
        if not isinstance(language, Language):
            language = Language.get(language)
        self.language = language

    @classmethod
    def __from_jsonld__(
        cls,
        document: Mapping[str, Any],
        loader: Optional[DocumentLoader] = None,
    ) -> Self:
        return cls(document["@value"], document["@language"])

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, type(self))
            and super().__eq__(other)
            and self.language == other.language
        )

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return super().__hash__() ^ hash(self.language)

    def __jsonld__(self, **kwargs: Any) -> Mapping[str, Any]:
        return {"@value": str(self), "@language": str(self.language)}

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({super().__repr__()},"
            f" language={str(self.language)!r})"
        )
