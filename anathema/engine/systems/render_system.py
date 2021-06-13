from __future__ import annotations
from anathema.engine.systems.base_system import BaseSystem


class RenderSystem(BaseSystem):

    def initialize(self):
        self.query("actors", all_of = [ "Actor", "Renderable" ])
        self.query("area", all_of = [ "EnvTilemap", "EnvIsCurrent" ])

    def draw_tiles(self):
        self.engine.renderer.render_tile_map(self.queries["area"].result[0])

    def draw_items(self):
        pass

    def draw_actors(self):
        current_area = self.queries["area"].result[0]
        cam_x, cam_y = self.engine.camera.camera_pos
        actors = self.queries["actors"].result
        for actor in actors:
            x, y = actor["Position"].xy
            if current_area.visible[y, x]:
                self.engine.console.tiles_rgb[["ch", "fg"]][y - cam_y, x - cam_x] = (
                    actor["Renderable"].char,
                    actor["Renderable"].fg
                )

    def update(self):
        self.loop.console.root.clear()
        self.draw_tiles()
        self.draw_actors()
