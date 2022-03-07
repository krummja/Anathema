from __future__ import annotations
from typing import Tuple, Optional, TYPE_CHECKING
import numpy as np
import json

from anathema.lib.ecstremity import Component
from anathema.engine.environments.tile import tile_dt
from anathema.data.tiles import tile_registry


if TYPE_CHECKING:
    from numpy.lib.index_tricks import IndexExpression


class Location:

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @property
    def xy(self) -> Tuple[int, int]:
        return self.x, self.y

    @xy.setter
    def xy(self, value: Tuple[int, int]) -> None:
        self.x, self.y = value

    @property
    def ij(self) -> Tuple[int, int]:
        return self.y, self.x

    def distance_to(self, x: int, y: int) -> int:
        return max(abs(self.x - x), abs(self.y - y))

    def relative(self, x: int, y: int) -> Location:
        return Location(self.x + x, self.y + y)

    def adjacent(self) -> IndexExpression:
        return np.s_[self.y-1:self.y+1, self.x-1:self.x+1]


class AreaLocation(Location):

    def __init__(self, tile_map: TileMap, x: int, y: int) -> None:
        self.tile_map = tile_map
        super().__init__(x, y)


class EnvTilemap(Component):

    def __init__(
            self,
            width: int,
            height: int,
    ) -> None:
        self.width = width
        self.height = height
        self._tiles = np.zeros(self.shape, dtype=tile_dt)
        self._explored = np.zeros(self.shape, dtype=bool)
        self._visible = np.zeros(self.shape, dtype=bool)
        self._actors = set()

    def __getstate__(self):
        state = super().__getstate__()
        tiles = []
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                tiles.append(int(self._tiles[x, y]["tid"]))
        state["_tiles"] = tiles
        return state

    def __setstate__(self, state):
        super().__setstate__(state)
        tile_list = state["_tiles"]
        meta_list = []
        for tile_index in tile_list:
            meta_list.append(tile_registry[tile_index])
        tile_array = np.array(meta_list, dtype=tile_dt)
        tile_array.reshape(self.shape)
        self._tiles = tile_array

    @property
    def actors(self):
        return self._actors

    @property
    def shape(self) -> Tuple[int, int]:
        return self.height, self.width

    @property
    def tiles(self) -> np.ndarray:
        return self._tiles

    @property
    def is_explored(self) -> np.ndarray:
        return self._explored

    @is_explored.setter
    def is_explored(self, value: np.ndarray) -> None:
        self._explored = value

    @property
    def is_visible(self) -> np.ndarray:
        return self._visible

    @is_visible.setter
    def is_visible(self, value: np.ndarray) -> None:
        self._visible = value

    def is_blocked(self, x: int, y: int) -> bool:
        # Constraint movement to the area
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True
        # If no move_cost, we can't move through the tile
        if not self.tiles[y, x]["move_cost"]:
            return True
        # If an actor occupies the tile, it's blocked
        # TODO Make this so that you swap with the actor if friendly?
        if any(actor["Position"].xy == (x, y) for actor in self.actors):
            return True
        return False

    def setup_terrain(self):
        evt = self.entity.fire_event("setup_terrain", data = {
            "tiles": self.tiles,
            "width": self.width,
            "height": self.height
        })

    def on_finalize(self, evt):
        self._tiles = evt.data.tiles

    def __getitem__(self, key: Tuple[int, int]) -> AreaLocation:
        return AreaLocation(self, *key)
