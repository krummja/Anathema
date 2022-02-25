from __future__ import annotations


class Shape(tuple):
    """Base class all other shapes are derived from."""

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def floored(self):
        raise NotImplementedError()
