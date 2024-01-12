from datetime import datetime
from typing import TypeAlias

from isoduration.types import Duration
from langcodes import Language

from ..uri import Uri
from .langstr import LanguageString

__all__ = ["ScalarValue"]

#: A type alias for scalar values.
ScalarValue: TypeAlias = (
    Uri
    | str
    | int
    | float
    | bool
    | datetime
    | Language
    | LanguageString
    | Duration
)
