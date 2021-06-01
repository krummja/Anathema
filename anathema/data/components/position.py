from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np

# type: Component
from ecstremity import Component

if TYPE_CHECKING:
    from numpy.lib.index_tricks import IndexExpression


class Position(Component):

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @property
    def xy(self):
        return self.x, self.y

    @property
    def ij(self):
        return self.y, self.x

    def distance_to(self, x: int, y: int) -> int:
        return max(abs(self.x - x), abs(self.y - y))

    def adjacent(self) -> IndexExpression:
        return np.s_[self.y-1:self.y+1, self.x-1:self.x+1]
