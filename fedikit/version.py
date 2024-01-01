__all__ = ["VERSION", "VERSION_INFO"]

VERSION_INFO = (0, 1, 0)
VERSION = (
    "{}.{}.{}".format(*VERSION_INFO)
    if len(VERSION_INFO) == 3
    else "{}.{}.{}-dev{}+{}".format(*VERSION_INFO)
)
