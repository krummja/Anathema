from __future__ import annotations
from typing import *
from anathema.lib.morphism import *

from gui.screen import Screen
import numpy as np
from math import ceil
from tcod import color
from anathema.prepare import CONSOLE_SIZE
from anathema.engine.environments.tile import tile_graphic


if TYPE_CHECKING:
    from anathema.engine.environments.generation.planet.generator import PlanetView
    from anathema.client import Client


RENDER_CONFIGURATION = {
    'Palette': {
        'Normal': np.array([
            (ord("≈"), color.Color( 20,  40, 130), color.Color(21, 21, 21)),
            (ord("≈"), color.Color( 20,  60, 165), color.Color(21, 21, 21)),
            (ord("≈"), color.Color( 60, 100, 210), color.Color(21, 21, 21)),
            (ord("2"), color.Color(175, 215, 170), color.Color(21, 21, 21)),
            (ord("3"), color.Color(125, 200, 140), color.Color(21, 21, 21)),
            (ord("4"), color.Color(100, 175, 100), color.Color(21, 21, 21)),
            (ord("5"), color.Color(100, 135,  95), color.Color(21, 21, 21)),
            (ord("6"), color.Color( 60, 110,  55), color.Color(21, 21, 21)),
            (ord("7"), color.Color( 30,  90,  25), color.Color(21, 21, 21)),
            (ord("8"), color.Color( 30,  65,  30), color.Color(21, 21, 21)),
            (ord("▲"), color.Color(120, 120, 120), color.Color(21, 21, 21)),
            (ord("▲"), color.Color(190, 190, 190), color.Color(21, 21, 21)),
        ], dtype = tile_graphic),
    }
}


class WorldCreation(Screen):

    def __init__(self, client: Client) -> None:
        super().__init__(client)
        self.position = (ceil(100 // 2), ceil(50 // 2))
        self.configuration = {
            "View": "Standard",
            "Palette": "Normal"
        }
        self.view: PlanetView | None = None

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    def on_enter(self, *args: List[Any]) -> None:
        self.view = self.client.loop.world_manager.viewer
        self.generate()
        self.client.loop.camera.camera_pos = self.position

    def pre_update(self) -> None:
        self.client.loop.console.clear(bg=(21, 21, 21))
        screen_view, world_view = self.client.loop.camera.camera_view(self.view.width, self.view.height, *CONSOLE_SIZE)
        self.client.loop.console.root.rgb[screen_view] = self.view.view[world_view]
        cam_x, cam_y = self.client.loop.camera.camera_pos
        x = self.position[0] - cam_x
        y = self.position[1] - cam_y
        self.client.loop.console.root.rgb[["fg", "bg"]][y][x] = (0, 0, 0), (255, 0, 0)

    def post_update(self) -> None:
        pass
        # world_data = self.view.world_data

    def cmd_move(self, direction):
        WIDTH = self.client.loop.world_manager.generator.width
        HEIGHT = self.client.loop.world_manager.generator.height
        target_x = self.x + direction[0]
        target_y = self.y + direction[1]
        if 0 <= target_x < WIDTH and 0 <= target_y < HEIGHT:
            self.position = (target_x, target_y)
            self.client.loop.camera.camera_pos = self.position

    def set_option(self, key, value):
        pass

    def generate(self):
        self.client.loop.world_manager.generator.generate()
        self.view.generate_standard_view(
            RENDER_CONFIGURATION["Palette"][self.configuration["Palette"]]
        )
        self.client.loop.console.clear(bg=(21, 21, 21))

    def get_current_view(self):
        if self.configuration["View"] == "Standard":
            self.view.generate_standard_view(
                RENDER_CONFIGURATION["Palette"][self.configuration["Palette"]]
            )

    def cmd_quit(self):
        self.client.screens.replace_screen("main")


