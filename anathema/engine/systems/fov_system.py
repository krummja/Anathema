from __future__ import annotations
import tcod
from anathema.engine.systems.base_system import BaseSystem


class FOVSystem(BaseSystem):

    def initialize(self):
        self.query("pov", all_of=[ "IsPlayer" ])
        # self.query("area", all_of = [ "EnvTilemap", "EnvIsCurrent" ])

    def update_fov(self):
        player = self.queries["pov"].result[0]
        # current_area = self.queries["area"].result[0]["EnvTilemap"]
        current_area = self.loop.area_system.current_area["EnvTileMap"]

        current_area.visible = tcod.map.compute_fov(
            transparency = current_area.tiles["transparent"],
            pov = player["Position"].ij,
            radius = player["Eyes"].sight_range,
            light_walls = True,
            algorithm = tcod.FOV_RESTRICTIVE
        )

        current_area.explored |= current_area.visible

    def update(self):
        self.loop.camera.camera_pos = self.queries["pov"].result[0]["Position"].xy
        self.update_fov()
