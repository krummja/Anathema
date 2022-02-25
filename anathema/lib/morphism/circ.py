from __future__ import annotations
from typing import Type, Union

from numbers import Real
import math

import numpy as np

from .shape import Shape
from .point import Point
from .size import Size
from .span import Span


class Circ(Shape):
    """Representation of a circle."""

    def __new__(cls: Type[Circ], origin: Point, radius: Size) -> Circ:
        cls._origin = origin
        cls._radius = radius
        return super().__new__(cls, (origin, radius))

    def __getnewargs__(self):
        return self._origin, self._radius

    def __contains__(self, other: object) -> bool:
        # TODO Implement
        pass

    @classmethod
    def from_edges(cls, *, top: Real, left: Real, radius: Real) -> Circ:
        return Circ(Point(left+radius, top+radius), Size(radius, radius))

    @classmethod
    def from_span(cls, *, span: Span) -> Circ:
        pass

    @classmethod
    def centered_at(cls, *, radius: Real, center: Point) -> Circ:
        left = center.x - radius
        top = center.y - radius
        return cls.from_edges(top=top, left=left, radius=radius)

    @property
    def radius(self) -> Real:
        return self[1].width

    @property
    def diameter(self) -> Real:
        return self[1].width * 2

    @property
    def circumference(self):
        return round((2 * math.pi * self.radius), 2)

    @property
    def area(self):
        return round((math.pi * (self.radius ** 2)), 2)

    @property
    def left(self):
        return self[0].x - self.radius

    @property
    def top(self):
        return self[0].y - self.radius

    @property
    def center(self):
        return self[0]

    @property
    def inner(self):
        xc, yc = self.center
        x, y = np.ogrid[:256, :256]
        dist_from_center = np.sqrt((x - xc)**2 + (y - yc)**2)
        return dist_from_center <= self.radius - 1

    @property
    def outer(self):
        """Get a NumPy mask array for the points inside the circle.
        Based on: https://stackoverflow.com/a/44874588
        """
        xc, yc = self.center
        x, y = np.ogrid[:256, :256]
        dist_from_center = np.sqrt((x - xc)**2 + (y - yc)**2)
        return dist_from_center <= self.radius

    @property
    def floored(self):
        return Circ(self._origin.floored, self._radius.floored)

    def distance_to(self, other: Circ) -> float:
        x, y = self.center
        other_x, other_y = other.center
        return abs(other_x - x) + abs(other_y - y)

    def nearest_distance(self, other: Circ) -> float:
        pass

    def replace(self, *, top: int = None, left: int = None, radius: int = None) -> Circ:
        if top is None:
            top = self.top
        if left is None:
            left = self.left
        if radius is None:
            radius = self.radius
        return type(self).from_edges(top=top, left=left, radius=radius)

    def shrink(self, *args):
        # TODO Implement
        pass

    def intersects(self, other: Union[Circ, Point]) -> bool:
        """Return True if this Circ overlaps with another at any point."""
        x, y = self.center
        if isinstance(other, Circ):
            other_x, other_y = other.center
            radii_sum_square = (self.radius + other.radius) ** 2
            dist_square = ((x - other_x) ** 2) + ((y - other_y) ** 2)
            if dist_square >= radii_sum_square:
                return False
        elif isinstance(other, Point):
            other_x, other_y = other.xy
            dist_square = ((x - other_x) ** 2) + ((y - other_y) ** 2)
            if dist_square >= self.radius:
                return False
        return True
