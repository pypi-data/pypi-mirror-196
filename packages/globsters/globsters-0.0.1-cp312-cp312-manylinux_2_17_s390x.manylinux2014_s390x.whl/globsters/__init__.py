from __future__ import annotations
from typing import Sequence
from .globsters import *

__version__ = __version_lib__
__all__ = ("__version__",)


def globster(pattern: str, case_insensitive: bool = False):
    return globsters.Globster(pattern, case_insensitive)


# def glob(patterns: Sequence[str], case_insensitive: bool = True) -> Globsters:
#     """Create a globset from a sequence of glob patterns.

#     :param patterns: A sequence of glob patterns.
#     :param case_sensitive: Whether the glob patterns should be case sensitive.
#     :return: A :class:`PyGlobset` instance.
#     """
#     if isinstance(patterns, str):
#         raise TypeError("patterns must be a sequence of strings")
#     return Globsters(patterns, case_insensitive)

__doc__ = globsters.__doc__
if hasattr(globsters, "__all__"):
    __all__ = globsters.__all__
