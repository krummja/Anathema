from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np

from anathema.lib.ecstremity import Component
from anathema.engine.environments.generation import array_tools, automata
from anathema.data.tiles import tile_registry

if TYPE_CHECKING:
    from anathema.lib.ecstremity import EntityEvent


class EnvTerrain(Component):

    def on_setup_terrain(self, evt: EntityEvent):
        tiles = evt.data.tiles
        _automata = automata.Anneal((evt.data.width, evt.data.height), density = 0.46)
        _automata.generate(10)

        result = _automata.board
        result = np.where(result == 1, tile_registry["Loose Dirt"].make(), tile_registry["unformed"].make())
        tiles[:] = result

        tiles = array_tools.rng_selection(
            tiles,
            tile_registry["unformed"],
            tile_registry["Packed Dirt"],
            [(10, tile_registry["Evergreen Tree"]),
             (20, tile_registry["Grass"]),
             (40, tile_registry["Tall Grass"])]
        )
        self.entity.fire_event("finalize", data = {"tiles": tiles})

    def on_get_entity_at_position(self, evt: EntityEvent):
        position = evt.data.position
        # self.entity.fire_event("found_entity", data = {"entity": })
