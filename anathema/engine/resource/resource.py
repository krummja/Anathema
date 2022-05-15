from __future__ import annotations

import math
from typing import *
from anathema.lib import math_utils
from . import T

if TYPE_CHECKING:
    from .tag import Tag


class Resource(Generic[T]):

    def __init__(
            self,
            obj: T,
            start_depth: int,
            end_depth: int,
            start_freq: float,
            end_freq: float
        ) -> None:
        self.obj = obj
        self.start_depth = start_depth
        self.end_depth = end_depth
        self.start_freq = start_freq
        self.end_freq = end_freq

        self._tags = Set[Tag[T]] = set()

    @property
    def tags(self) -> Set[Tag[T]]:
        return self._tags

    def frequency_at_depth(self, depth: int) -> float:
        if self.start_depth == self.end_depth:
            return self.start_freq
        return math_utils.lerp_float(
            depth,
            self.start_depth,
            self.end_depth,
            self.start_freq,
            self.end_freq
        )

    def chance_at_depth(self, depth: int) -> float:
        if depth < self.start_depth:
            relative = self.start_depth - depth
            deviation = 0.6 + depth * 0.2
            return math.exp(-0.5 * relative * relative / (deviation * deviation))
        elif depth > self.end_depth:
            relative = depth - self.end_depth
            deviation = 1.0 + depth * 0.1
            return math.exp(-0.5 * relative * relative / (deviation * deviation))
        return 1.0
