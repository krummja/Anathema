from __future__ import annotations
from typing import Tuple, Optional
import numpy as np

from anathema.engine.environments.tile_type import TileType
from anathema.constants.color import Color


class TileRegistry:

    def __init__(self) -> None:
        self._last_index = 0
        self._tiles = {}
        self._mapping = {}

    def key_to_index(self, key: str) -> int:
        return self._mapping[key]

    def index_to_key(self, index: int) -> str:
        return self._mapping[index]

    def add_tile(
            self,
            key: str,
            char: str,
            fore: Tuple[int, int, int],
            back: Optional[Tuple[int, int, int]] = None,
            *,
            open: bool = False,
            solid: bool = False,
            obstacle: bool = False,
            obfuscated: bool = False,
            passable: bool = False,
            opaque: bool = False,
        ) -> None:
        self._mapping[self._last_index] = key
        self._mapping[key] = self._last_index

        tile = TileType(self._last_index, char, fore, back if back else (21, 21, 21))
        tile = tile.open() if open else tile
        tile = tile.solid() if solid else tile
        tile = tile.obstacle() if obstacle else tile
        tile = tile.obfuscated() if obfuscated else tile
        tile = tile.passable() if passable else tile
        tile = tile.opaque() if opaque else tile

        self._tiles[key] = tile
        self._last_index += 1

    def __getitem__(self, key_or_index) -> np.ndarray:
        if isinstance(key_or_index, str):
            return self._tiles[key_or_index]
        if isinstance(key_or_index, int):
            key = self._mapping[key_or_index]
            return self._tiles[key]


tile_registry = TileRegistry()

tile_registry.add_tile("unformed", "?", Color.light_cool_gray, open = True)
tile_registry.add_tile("unformed_wet", "≈", Color.light_blue, open = True)
tile_registry.add_tile("open", ".", Color.white, open = True)
tile_registry.add_tile("solid", "#", Color.light_cool_gray, solid = True)
tile_registry.add_tile("passage", "-", Color.light_cool_gray, open = True)
tile_registry.add_tile("solid_wet", "≈", Color.cool_gray, obstacle = True)
tile_registry.add_tile("passage_wet", "≈", Color.light_blue, open = True)
tile_registry.add_tile("doorway", "○", Color.light_cool_gray, open = True)

tile_registry.add_tile("Flagstone Wall", "▒", Color.light_warm_gray, Color.warm_gray, solid = True)
tile_registry.add_tile("Granite Wall", "▒", Color.cool_gray, solid = True)
tile_registry.add_tile("Granite", "▓", Color.dark_cool_gray, solid = True)

tile_registry.add_tile("Flagstone Floor", ".", Color.warm_gray, Color.dark_warm_gray, open = True)
tile_registry.add_tile("Granite Floor", ".", Color.dark_cool_gray, Color.darker_cool_gray, open = True)

tile_registry.add_tile("Loose Dirt", "·", Color.brown, open = True)
tile_registry.add_tile("Packed Dirt", "φ", Color.brown, open = True)
tile_registry.add_tile("Grass", "░", Color.lima, open = True)
tile_registry.add_tile("Tall Grass", "√", Color.pea_green, obfuscated = True)
tile_registry.add_tile("Evergreen Tree", "▲", Color.sherwood, solid = True)
tile_registry.add_tile("Shallow Water", "≈", Color.light_blue, open = True)
