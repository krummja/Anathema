from __future__ import annotations
from typing import *
from anathema.lib.morphism import *

from anathema.gui.views import *
import asyncio
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

        self.info_panel = RectView(size = Size(-1, 4))
        self.add_view(self.info_panel)
        Snap(self.info_panel).top().center()

        self.lat_label = TextField(text="")
        self.add_view(self.lat_label)
        Snap(self.lat_label).top(1).left(2)

        self.long_label = TextField(text="")
        self.add_view(self.long_label)
        Snap(self.long_label).top(2).left(2)

        self.biome_label = TextField(text="")
        self.add_view(self.biome_label)

        # self.temperature_label = TextField(text="")
        # self.add_view(self.temperature_label)

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
        world_data = self.view.world_data
        self.lat_label.update_label(self.tile_to_coord(0, self.y))
        self.long_label.update_label(self.tile_to_coord(1, self.x))
        self.biome_label.update_label(self.biome_name(world_data[self.y][self.x]['biome_id']))
        Snap(self.biome_label).top(1).right(len(self.biome_label.text) + 2)
        # self.temperature_label.update_label(str(round(world_data[self.y][self.x]['temperature'], 2)))
        # Snap(self.temperature_label).top(2).right(len(self.temperature_label.text) + 2)

    def set_option(self, key, value):
        self.configuration[key] = value

    def generate(self):
        asyncio.run(self.client.loop.world_manager.generator.generate())
        self.get_current_view()
        self.client.loop.console.clear(bg=(21, 21, 21))

    def get_current_view(self):
        if self.configuration["View"] == "Standard":
            self.view.generate_standard_view(
                RENDER_CONFIGURATION["Palette"][self.configuration["Palette"]]
            )

    def tile_to_coord(self, lat_long: int, tile: int) -> str:
        suf = (("N", "S"), ("W", "E"))[lat_long]
        coord = (tile * 360) / (100, 200)[lat_long]
        if coord < 180:
            return "{:4}".format(str(int(180 - coord))) + suf[0]
        if coord > 180:
            return "{:4}".format(str(int(coord - 180))) + suf[1]
        return ("- EQUATOR -", "- MERIDIAN -")[lat_long]

    def biome_name(self, biome_id: int) -> str:
        return {
            0: "ice cap",
            1: "tundra",
            2: "subarctic",
            3: "dry steppe",
            4: "dry desert",
            5: "highland",
            6: "humid continental",
            7: "dry summer subtropic",
            8: "tropical wet & dry",
            9: "marine west coast",
            10: "humid subtropical",
            11: "wet tropics",
            12: "ocean",
            13: "shallow ocean"
        }[biome_id]

    def cmd_move(self, direction):
        WIDTH = self.client.loop.world_manager.generator.width
        HEIGHT = self.client.loop.world_manager.generator.height
        target_x = self.x + direction[0]
        target_y = self.y + direction[1]
        if 0 <= target_x < WIDTH and 0 <= target_y < HEIGHT:
            self.position = (target_x, target_y)
            self.client.loop.camera.camera_pos = self.position

    def cmd_confirm(self):
        environs = {}
        for y in range(self.y - 1, self.y + 1):
            for x in range(self.x - 1, self.x + 1):
                environs[(y, x)] = self.view.world_data[y][x]
        selection = environs[(self.y, self.x)]
        self.client.loop.world_manager.region_builder.new_region(selection, environs)

    def cmd_quit(self):
        self.client.screens.replace_screen("main")
