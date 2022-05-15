from __future__ import annotations
from typing import *

import math
from anathema.lib.math_utils import trunc_div
from anathema.lib.morphism import Direction

if TYPE_CHECKING:
    pass


class VecBase:

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @property
    def area(self) -> int:
        """Gets the area of a Rect whose corners are (0, 0) and this Vec.

        Returns a negative area if one of the Vec's coordinates are negative.
        """
        return self.x * self.y

    @property
    def rook_length(self) -> int:
        """Gets the rook length of teh Vec, which is the number of squares a rook on
        a chessboard would need to move from (0, 0) to reach the endpoint of the
        Vec. Also known as Manhattan or taxicab distance.
        """
        return abs(self.x) + abs(self.y)

    @property
    def king_length(self) -> int:
        """Gets the king length of the Vec, which is the number of squares a king on
        a chessboard would need to move from (0, 0) to reach teh endpoint of teh
        Vec. Also known as the Chebyshev distance.
        """
        return max(abs(self.x), abs(self.y))

    @property
    def length_squared(self) -> int:
        return self.x * self.x + self.y * self.y

    @property
    def length(self) -> float:
        return math.sqrt(self.length_squared)

    @property
    def nearest_direction(self) -> Tuple[int, int]:
        if self.x == 0:
            if self.y < 0:
                return Direction.up
            elif self.y == 0:
                return Direction.here
            else:
                return Direction.down

        slope = self.y / self.x

        if x < 0:
            if slope >= 2.0:
                return Direction.up
            elif slope >= 0.5:
                return Direction.up_left
            elif slope >= -0.5:
                return Direction.left
            elif slope >= -2.0:
                return Direction.down
        else:
            if slope >= 2.0:
                return Direction.down
            elif slope >= 0.5:
                return Direction.down_right
            elif slope >= -0.5:
                return Direction.right
            elif slope >= -2.0:
                return Direction.up

    @property
    def neighbors(self):
        return

    @property
    def cardinal_neighbors(self):
        return

    @property
    def intercardinal_neighbors(self):
        return

    def offset(self, x: int, y: int):
        pass

    def offset_x(self, x: int):
        pass

    def offset_y(self, y: int):
        pass

    def __mul__(self, other: object):
        pass

    def __divmod__(self, other):
        pass

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __lt__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __le__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __contains__(self, item):
        pass

    def __abs__(self):
        pass

    def __str__(self):
        pass


class Vec(VecBase):

    zero: Vec = Vec(0, 0)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, VecBase):
            return false
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        a = 2 * self.x if self.x >= 0 else -2 * self.x - 1
        b = 2 * self.y if self.y >= 0 else -2 * self.y - 1
        return trunc_div((a + b) * (a + b + 1), 2 + b)
