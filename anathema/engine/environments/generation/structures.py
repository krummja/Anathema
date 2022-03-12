from __future__ import annotations
from typing import *

import random
import numpy as np

from anathema.data.tiles import tile_registry
from anathema.lib.morphism import *


def build_room(
        tiles: np.ndarray,
        point: Point,
        size: Size,
    ) -> np.ndarray:
    space = Rect(point - 1, size + 2)
    tiles[space.outer] = tile_registry["Loose Dirt"].make()

    room = Rect(point, size)
    tiles[room.outer] = tile_registry["Flagstone Wall"].make()
    tiles[room.inner] = tile_registry["Flagstone Floor"].make()

    wall = [p for p in room.edge_span(Direction.left)]
    door = wall[len(wall) // 2]
    tiles[door] = tile_registry["Flagstone Floor"].make()
    return tiles
