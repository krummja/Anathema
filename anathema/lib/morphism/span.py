from __future__ import annotations

from typing import *
from numbers import Real
import math

from .shape import Shape
from .point import Point


class Span(Shape):
    """Representation of a line segment defined by Point endpoints."""

    def __new__(cls: Type[Span], start: Point, end: Point) -> Span:
        return super().__new__(cls, (start, end))

    @property
    def start(self) -> Point:
        return self[0]

    @property
    def end(self) -> Point:
        return self[1]

    def __contains__(self, point: Point) -> bool:
        return self.start <= point <= self.end

    def __iter__(self) -> Generator[Point, None, None]:
        """for point in span..."""
        x_wise = range(self.start[0], self.end[0] + 1)
        y_wise = range(self.start[1], self.end[1] + 1)

        for x in x_wise:
            for y in y_wise:
                yield Point(x, y)

    def __len__(self) -> int:
        return int(math.sqrt((self.end[0] - (self.start[0] + 1))**2 +
                             (self.end[1] - (self.start[1] + 1))**2))

    def __add__(self, n) -> Span:
        if isinstance(n, Real):
            return Span(self.start + n, self.end + n)
        return NotImplemented

    def __sub__(self, n) -> Span:
        return self - n

    @property
    def floored(self) -> Span:
        return Span(self.start.floored, self.end.floored)

    def overlaps(self, other) -> bool:
        return self.start <= other.end and self.end >= other.start

    # def shift_into_view(self, point, *, margin=0) -> Span:
    #     if self.start + margin <= point <= self.end - margin:
    #         return self
    #     assert isinstance(point, int)
    #     assert isinstance(margin, int)
    #     assert margin > 0
    #     d = (min(0, point - (self.start + margin)) +
    #          max(0, point - (self.end - margin)))
    #     return self + d
    #
    # def scale(self, width, *, pivot=None) -> Span:
    #     old_width = len(self)
    #     if old_width == width:
    #         return self
    #     if pivot is None:
    #         pivot = (self.start + self.end) // 2
    #
    #     relative_pos = (pivot - self.start) / old_width
    #     start_offset = relative_pos * width
    #     if relative_pos <= 0.5:
    #         start_offset = int(start_offset + 0.5)
    #     else:
    #         start_offset = int(start_offset)
    #
    #     start = pivot - start_offset
    #     end = start + width - 1
    #     return Span(start, end)
