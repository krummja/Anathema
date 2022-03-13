from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from anathema.data.tiles import tile_registry
from anathema.engine.environments.generation import array_tools, automata
from anathema.engine.environments.generation.structures import build_room
from anathema.lib.ecstremity import Component
from anathema.lib.morphism import *

if TYPE_CHECKING:
    from anathema.lib.ecstremity import EntityEvent


class EnvTerrain(Component):

    def on_setup_terrain(self, evt: EntityEvent):
        tiles = evt.data.tiles
        _automata = automata.Anneal((evt.data.width, evt.data.height), density = 0.46)
        _automata.generate(10)

        result = _automata.board
        result = np.where(result == 1, tile_registry["Shallow Water"].make(), tile_registry["unformed"].make())
        tiles[:] = result

        tiles = array_tools.rng_selection(
            tiles,
            tile_registry["unformed"],
            tile_registry["Packed Dirt"],
            [
                (10, tile_registry["Tall Grass"]),
                (20, tile_registry["Evergreen Tree"]),
                (70, tile_registry["Grass"]),
                (80, tile_registry["Flowers"]),
             ]
        )

        tiles = build_room(tiles, Point(5, 5), Size(15, 15))
        # tiles[10:12, 10:12] = tile_registry["Test Tile 2"].make()

        self.entity.fire_event("finalize", data = {"tiles": tiles})
