from __future__ import annotations
from typing import *

import random
from . import T

from anathema.lib import rng, math_utils

if TYPE_CHECKING:
    from .resource import Resource
    from .query_key import QueryKey

from random import Random
from math import floor, ceil


class ResourceQuery(Generic[T]):

    def __init__(
            self,
            depth: int,
            resources: List[Resource[T]],
            chances: List[float],
            total_chance: float
        ) -> None:
        self.depth = depth
        self.resources = resources
        self.chances = chances
        self.total_chance = total_chance

    def choose(self) -> T | None:
        if not self.resources:
            return None

        t = rng.rand_float(self.total_chance)
        first = 0
        last = len(self.resources) - 1
        while True:
            middle = math_utils.trunc_div((first + last), 2)
            if middle > 0 and t < self.chances[middle - 1]:
                last = middle - 1
            elif t < self.chances[middle]:
                return self.resources[middle].obj
            else:
                first = middle + 1

    def dump(self, key: QueryKey) -> None:
        print(key)
        for i, _ in enumerate(self.resources):
            chance = self.chances[i]
            if i > 0:
                chance -= self.chances[i - 1]
            percent = str((100.0 * chance / self.total_chance)).zfill(8)
            print(f"{percent} {self.resources[i].obj}")
