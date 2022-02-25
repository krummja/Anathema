from __future__ import annotations
from typing import *
from numbers import Real
from math import floor
from typing import Type

from .shape import Shape


class Size(Shape):
    """Base class for defining a 2D area.

    Supports floor division.
    """

    def __new__(cls: Type[Size], width: Real = 0, height: Real = 0) -> Size:
        return super().__new__(cls, (width, height))

    def __add__(self, other: Union[Size, Real]) -> Union[Size, Real]:
        if isinstance(other, Size):
            return self.area + other.area
        else:
            return Size(self.width + other, self.height + other)

    def __sub__(self, other: Union[Size, Real]) -> Union[Size, Real]:
        if isinstance(other, Size):
            return self.area - other.area
        else:
            return Size(self.width - other, self.height - other)

    def __floordiv__(self, n) -> Size:
        if not isinstance(n, Real):
            return NotImplemented
        return Size(self[0] // n, self[1] // n)

    @property
    def area(self) -> Real:
        return self.width * self.height

    @property
    def floored(self) -> Size:
        """A copy of this rect with the :py:attr:`Point.floored` origin/size
        copies"""
        return Size(floor(self.width), floor(self.height))

    @property
    def height(self) -> Real:
        return self[1]

    @property
    def width(self) -> Real:
        return self[0]
