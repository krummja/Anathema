from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

from morphism import *
import numpy as np

from anathema.engine.environments.tile import tile_graphic

if TYPE_CHECKING:
    from anathema.data.components.envtilemap import EnvTilemap
    from anathema.console import Console
    from anathema.engine.engine import EngineLoop


class Renderer:

    def __init__(self, loop: EngineLoop) -> None:
        self.loop = loop

    @property
    def console(self) -> Console:
        return self.loop.console

    def render_tile_map(self, tile_map: EnvTilemap) -> None:
        screen_view, world_view = self.loop.camera.camera_view(tile_map.width, tile_map.height)
        self.console.tiles_rgb[screen_view] = self.select_area_mask(tile_map, world_view)

    @staticmethod
    def select_area_mask(tile_map: EnvTilemap, world_view: Tuple[slice, slice]) -> np.ndarray:
        UNKNOWN = np.asarray((0, (21, 21, 21), (21, 21, 21)), dtype=tile_graphic)

        if_visible = tile_map.visible[world_view]
        if_explored = tile_map.explored[world_view]
        lit_tiles = tile_map.tiles["light"][world_view]
        unlit_tiles = tile_map.tiles["dark"][world_view]

        condlist = (if_visible, if_explored)
        choicelist = (lit_tiles, unlit_tiles)

        return np.select(condlist, choicelist, UNKNOWN)  # type: ignore
