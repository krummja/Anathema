from __future__ import annotations
from typing import Tuple
import numpy as np


tile_graphic = np.dtype([
    ("ch", int),
    ("fg", "3B"),
    ("bg", "3B"),
])


tile_dt = np.dtype([
    ("tid", int),
    ("move_cost", np.uint8),
    ("transparent", bool),
    ("light", tile_graphic),
    ("dark", tile_graphic),
])


def define_tile(
        tid: int,
        move_cost: int,
        transparent: bool,
        char: int,
        color: Tuple[int, int, int],
        bg: Tuple[int, int, int],
    ) -> np.ndarray:
    light = (char, color, bg)
    dark = (char, (color[0] // 2, color[1] // 2, color[2] // 2), (21, 21, 21))
    tile_data = np.array((int(tid), move_cost, transparent, light, dark), dtype=tile_dt)
    return tile_data
