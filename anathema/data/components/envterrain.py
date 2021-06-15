from __future__ import annotations
from typing import TYPE_CHECKING

from ecstremity import Component
import numpy as np

from anathema.engine.environments.generation import array_tools, automata
from anathema.engine.environments.tile_defs import Tiles

if TYPE_CHECKING:
    from ecstremity import EntityEvent


class EnvTerrain(Component):

    def on_setup_terrain(self, evt: EntityEvent):
        tiles = evt.data.tiles
        _automata = automata.Anneal((evt.data.width, evt.data.height), density = 0.46)
        _automata.generate(10)

        result = _automata.board
        result = np.where(result == 1, Tiles.dirt_1.make(), Tiles.unformed.make())
        tiles[:] = result

        tiles = array_tools.rng_selection(
            tiles,
            Tiles.unformed,
            Tiles.dirt_2,
            [(10, Tiles.tree_1),
             (20, Tiles.grass),
             (40, Tiles.tall_grass)]
        )

        self.entity.fire_event("finalize", data = {"tiles": tiles})
