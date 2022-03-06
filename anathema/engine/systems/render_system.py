from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

import numpy as np
from anathema.lib.morphism import *
from anathema.engine.environments.tile import tile_graphic
from anathema.engine.systems.base_system import BaseSystem

if TYPE_CHECKING:
    from anathema.data.components.envtilemap import EnvTilemap
    from anathema.console import Console
    from anathema.engine.engine import EngineLoop


class RenderSystem(BaseSystem):

    def initialize(self):
        self.query("actors", all_of = [ "Actor", "Renderable" ])
        self.query("area", all_of = [ "EnvTilemap", "EnvIsCurrent" ])

    def draw_tiles(self):
        tile_map: EnvTilemap = self.queries["area"].result[0]["EnvTilemap"]
        screen_view, world_view = self.loop.camera.camera_view(tile_map.width, tile_map.height)
        UNKNOWN = np.asarray((0, (21, 21, 21), (21, 21, 21)), dtype=tile_graphic)

        if_visible = tile_map.is_visible[world_view]
        if_explored = tile_map.is_explored[world_view]
        lit_tiles = tile_map.tiles["light"][world_view]
        unlit_tiles = tile_map.tiles["dark"][world_view]

        condlist = (if_visible, if_explored)
        choice_list = (lit_tiles, unlit_tiles)
        tile_array = np.select(condlist, choice_list, UNKNOWN)
        self.loop.console.root.tiles_rgb[screen_view] = tile_array

    def draw_items(self):
        pass

    def draw_actors(self):
        current_area: EnvTilemap = self.queries["area"].result[0]["EnvTilemap"]
        cam_x, cam_y = self.loop.camera.camera_pos
        actors = self.queries["actors"].result

        for actor in actors:
            x, y = actor["Position"].xy
            if current_area.is_visible[y, x]:
                self.loop.console.root.tiles_rgb[["ch", "fg"]][y - cam_y, x - cam_x] = (
                    actor["Renderable"].char,
                    actor["Renderable"].fg
                )

    def update(self):
        self.loop.console.root.clear(bg = (21, 21, 21))
        self.draw_tiles()
        self.draw_actors()
