from datetime import datetime
from typing import TypeAlias

from langcodes import Language

from .langstr import LanguageString

__all__ = ["ScalarValue"]

#: A type alias for scalar values.
ScalarValue: TypeAlias = (
    str | int | bool | datetime | Language | LanguageString
)
