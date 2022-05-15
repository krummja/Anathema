from __future__ import annotations

import time
from typing import *

import numpy as np
import tcod

from anathema.engine.environments.tile import tile_graphic
from anathema.engine.systems.base_system import BaseSystem

if TYPE_CHECKING:
    from numpy.typing import NDArray
    from data.components.environment.envtilemap import EnvTilemap
    from anathema.lib.ecstremity import Entity


TORCH_RADIUS = 20
SQR_TORCH_RADIUS = TORCH_RADIUS * TORCH_RADIUS


NOISE = tcod.noise.Noise(1)


def compute_lighting(source: Entity, view: Tuple[slice, slice], fov: NDArray[np.bool]):
    origin = source["Position"]

    torch_t = time.perf_counter() * 5
    torch_x = origin.y + NOISE.get_point(torch_t) * 1.5
    torch_y = origin.x + NOISE.get_point(torch_t + 11) * 1.5
    brightness = 0.2 * NOISE.get_point(torch_t + 17)

    x, y = np.mgrid[view]
    x = x.astype(np.float32) - torch_x
    y = y.astype(np.float32) - torch_y

    dist_sqr = x**2 + y**2
    visible = (dist_sqr < SQR_TORCH_RADIUS) & fov

    light = SQR_TORCH_RADIUS - dist_sqr
    light /= SQR_TORCH_RADIUS
    light += brightness
    light.clip(0, 1, out=light)
    light[~visible] = 0

    return light


class RenderSystem(BaseSystem):

    torch: bool = False

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

        if self.torch:
            lighting = compute_lighting(self.loop.player.entity, world_view, if_visible)
            falloff = lighting[..., np.newaxis]
            tile_array["fg"] = np.where(if_visible[..., np.newaxis], tile_array["fg"] * falloff, tile_array["fg"])

        self.loop.console.root.rgb[screen_view] = tile_array

    def draw_items(self):
        pass

    def draw_actors(self):
        current_area: EnvTilemap = self.queries["area"].result[0]["EnvTilemap"]
        cam_x, cam_y = self.loop.camera.camera_pos
        actors = self.queries["actors"].result

        for actor in actors:
            x, y = actor["Position"].xy
            if current_area.is_visible[y, x]:
                self.loop.console.root.rgb[["ch", "fg"]][y - cam_y, x - cam_x] = (
                    actor["Renderable"].char,
                    actor["Renderable"].fg
                )

    def update(self):
        self.loop.console.root.clear(bg = (21, 21, 21))
        self.draw_tiles()
        self.draw_actors()
