from __future__ import annotations
from typing import Optional, Tuple
from dataclasses import dataclass
import numpy as np

from anathema.constants.color import Color
from anathema.engine.environments.tile import define_tile


@dataclass
class TileType:
    tid: int
    char: str
    fore: Tuple[int, int, int]
    back: Tuple[int, int, int]

    _passable: Optional[bool] = None
    _opaque: Optional[bool] = None

    def open(self) -> TileType:
        self._passable = True
        self._opaque = False
        return self

    def solid(self) -> TileType:
        self._passable = False
        self._opaque = True
        return self

    def obstacle(self) -> TileType:
        self._passable = False
        self._opaque = False
        return self

    def obfuscated(self) -> TileType:
        self._passable = True
        self._opaque = True
        return self

    def passable(self) -> TileType:
        self._passable = True
        return self

    def opaque(self) -> TileType:
        self._opaque = True
        return self

    def make(self) -> np.ndarray:
        move_cost = 1 if self._passable else 0
        transparent = not self._opaque
        back = self.back if self.back else (21, 21, 21)
        return define_tile(self.tid, move_cost, transparent, ord(self.char), self.fore, back)
