from __future__ import annotations
from typing import *

from anathema.console import console
from gui.screen import Screen
from anathema.gui.views import *
from anathema.lib.morphism import *
from anathema.prepare import CONSOLE_SIZE

if TYPE_CHECKING:
    from anathema.client import Client


class Stage(Screen):
    
    def __init__(self, client: Client) -> None:
        super().__init__(client)

        self.player = client.session.world.get_entity("PLAYER")
        self.player_name = self.player["Moniker"].name

        # self.left_panel = RectView(size = Size(20, CONSOLE_SIZE[1]), fg = (100, 100, 100))
        # self.add_view(self.left_panel)
        # Snap(self.left_panel).left()
        #
        # self.equipment = RectView(size = Size(26, CONSOLE_SIZE[1]), fg = (100, 100, 100))
        # self.add_view(self.equipment)
        # Snap(self.equipment).right()
        #
        # self.message_panel = RectView(size = Size(CONSOLE_SIZE[0] - 20 - 26, 16), fg = (100, 100, 100))
        # self.add_view(self.message_panel)
        # Snap(self.message_panel).bottom().left(20)

    def on_enter(self, *args: List[Any]) -> None:
        self.client.loop.is_running = True
        console.root.clear()

        self.client.loop.camera.camera_pos = self.client.loop.player.position
        self.client.loop.camera.view_rect = Rect(Point(21, 0), Size(CONSOLE_SIZE[0] - 20, CONSOLE_SIZE[1] - 16))
        self.client.loop.area_system.update()
        self.client.loop.fov_system.update_fov()
        self.client.loop.render_system.update()

    def on_leave(self, *args: List[Any]) -> None:
        self.client.loop.teardown()
        console.root.clear(bg = (21, 21, 21))

    def pre_update(self) -> None:
        self.client.loop.update()

    def post_update(self) -> None:
        pass
        # self.client.loop.camera.camera_debug()

    def cmd_move(self, delta: Tuple[int, int]) -> None:
        self.client.loop.player.move(delta)

    def cmd_quit(self) -> None:
        self.client.screens.pop_screen()
