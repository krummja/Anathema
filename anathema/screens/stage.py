from __future__ import annotations
from typing import TYPE_CHECKING, List, Tuple
import math

from morphism import (Rect, Size, Point)  # type: ignore

import tcod
from anathema.screen import Screen
from anathema.views.layout import Layout
from anathema.views.button_view import ButtonView
from anathema.views.rect_view import RectView
from anathema.views.label_view import LabelView
from anathema.prepare import CONSOLE_SIZE

from anathema.console import console

if TYPE_CHECKING:
    from anathema.client import Client
    from anathema.view import View


POSITION_RECT = Rect(Point(0, 0), Size(*CONSOLE_SIZE))
STAGE_RECT = Rect(Point(0, 0), Size(math.ceil(CONSOLE_SIZE[0] * 0.6), CONSOLE_SIZE[1]))


class Stage(Screen):

    def __init__(self, client: Client) -> None:

        self.player = client.session.world.get_entity("PLAYER")
        self.player_name = self.player["Moniker"].name

        self.views: List[View] = [
            LabelView(
                self.player_name,
                layout = Layout(top = 2, left = 2)
            )
        ]
        super().__init__(client=client, views=self.views)

    def on_enter(self, *args: List[Any]) -> None:
        self.client.loop.is_running = True

        console.root.clear()
        self.client.loop.camera.camera_pos = self.client.loop.player.position
        self.client.loop.area_system.update()
        self.client.loop.fov_system.update_fov()
        self.client.loop.render_system.update()

    def pre_update(self) -> None:
        self.client.loop.update()

    # region SCREEN COMMANDS
    def cmd_confirm(self):
        pass

    def cmd_cancel(self):
        self.client.pop_screen()

    def cmd_move(self, delta: Tuple[int, int]) -> None:
        self.client.loop.player.move(delta)
    # endregion
