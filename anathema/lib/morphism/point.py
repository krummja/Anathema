from __future__ import annotations
from numbers import Real
from math import floor
from typing import *

from .shape import Shape
from .direction import Direction
from .size import Size


class Point(Shape):
    """Representation of a point using integer values.

    A Point object is defined as a tuple encoding its x,y components.
    Points can be indexed in row-major order using the property `Point.ij`.
    """

    def __new__(cls: Type[Point], x: Real = 0, y: Real = 0) -> Point:
        return tuple.__new__(cls, (x, y))

    def __add__(self, other: Union[Point, Size, Direction, Real]) -> Point:
        """Add this point to the components of either another Point or a
        Direction.
        """
        if isinstance(other, Direction):
            other: Real = other.value
        elif isinstance(other, (Point, Size)):
            other: Tuple[Real, Real] = other
        elif isinstance(other, Real):
            other: Tuple[Real, Real] = (other, other)
        else:
            return NotImplemented
        return Point(self.x + other[0], self.y + other[1])

    def __sub__(self, other: Union[Point, Size, Direction, Real]) -> Point:
        """Subtract this Point from the components of either another Point,
        Size, Direction, or Real (int/float).
        """
        if isinstance(other, Direction):
            other: Tuple[Real, Real] = other.value
        elif isinstance(other, (Point, Size)):
            other: Tuple[Point, Size] = other
        elif isinstance(other, Real):
            other: Tuple[Real, Real] = (other, other)
        else:
            return NotImplemented
        return Point(self.x - other[0], self.y - other[1])

    @property
    def floored(self) -> Point:
        """A copy of this point with ``math.floor()`` called on each coordinate."""
        return Point(floor(self.x), floor(self.y))

    @property
    def neighbors(self) -> List[Point]:
        """Return a list of all neighboring Points."""
        return [self + d for d in Direction]

    @property
    def origin(self) -> Point:
        """Origin point of the coordinate plane."""
        return Point(0, 0)

    @property
    def x(self) -> Real:
        """Point object's x axis component."""
        return self[0]

    @property
    def y(self) -> Real:
        """Point object's y axis component."""
        return self[1]

    @property
    def xy(self) -> Tuple[Real, Real]:
        """Cartesian x,y coordinates of this Point."""
        return self[0], self[1]

    @property
    def ij(self) -> Tuple[Real, Real]:
        """Row-major ordered coordinates of this Point."""
        return self[1], self[0]
