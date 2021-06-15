from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from ecstremity import Component
import numpy as np
import json

from anathema.engine.environments.tile import tile_dt
from anathema.engine.environments.tile_defs import Tiles


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


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


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
        state["tiles"] = json.dumps(self._tiles, cls=NumpyEncoder)
        return state

    def __setstate__(self, state):
        super().__setstate__(state)
        self._tiles = np.array(state["tiles"])

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
    def explored(self) -> np.ndarray:
        return self._explored

    @explored.setter
    def explored(self, value: np.ndarray) -> None:
        self._explored = value

    @property
    def visible(self) -> np.ndarray:
        return self._visible

    @visible.setter
    def visible(self, value: np.ndarray) -> None:
        self._visible = value

    def is_blocked(self, x: int, y: int) -> bool:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True
        if not self.tiles[y, x]["move_cost"]:
            return True
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


# TODO Make a tile rebuilder from deserialized tile data
if __name__ == '__main__':
    tile = Tiles.tall_grass.make()
    json_tile = json.dumps(tile, cls=NumpyEncoder)
    print(json_tile)
    json_load = json.loads(json_tile)
    restored = np.asarray(json_load)
    print(restored)
