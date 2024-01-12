from typing import NewType

__all__ = ["Uri"]


#: A URI.
Uri = NewType("Uri", str)
