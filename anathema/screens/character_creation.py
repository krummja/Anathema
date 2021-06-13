from __future__ import annotations
from typing import TYPE_CHECKING, List, Tuple

from morphism import (Rect, Size, Point)  # type: ignore

import tcod
from anathema.screen import Screen
from anathema.views.layout import Layout
from anathema.views.button_view import ButtonView
from anathema.views.rect_view import RectView
from anathema.views.label_view import LabelView
from anathema.views.text_input import TextInputView, TextInputConfig
from anathema.prepare import CONSOLE_SIZE

from anathema.screens.stage import Stage

if TYPE_CHECKING:
    from anathema.client import Client
    from anathema.view import View


POSITION_RECT = Rect(Point(0, 0), Size(*CONSOLE_SIZE))


class CharacterCreation(Screen):

    def __init__(self, client: Client) -> None:

        self.character_info = {
            "name": ""
        }

        # region CHARACTER NAME
        self.text_input_box = RectView(
            layout = Layout(
                top = 2, right = None, bottom = None, left = 2,
                width = 30, height = 3),
            subviews = [
                LabelView(
                    "Name:",
                    align_horz = "left",
                    align_vert = "center",
                    layout = Layout(top = 1, left = 1)
                ),
                TextInputView(
                    config = TextInputConfig(),
                    callback = self.ui_set_player_name,
                    layout = Layout(top = 1, right = 1, bottom = 1, left = 7)
                ),
            ])
        # endregion

        self.continue_button = ButtonView(
            "Continue",
            self.ui_continue,
            align_horz = "left",
            align_vert = "bottom",
            layout = Layout(bottom = 8, left = 2))

        self.cancel_button = ButtonView(
            "Cancel",
            self.ui_cancel,
            align_horz = "left",
            align_vert = "bottom",
            layout = Layout(bottom = 6, left = 2))

        super().__init__(client=client, views=[RectView(
            layout = Layout(top = 0, left = 0),
            subviews = [self.text_input_box, self.continue_button, self.cancel_button]
        )])

    # region SCREEN COMMANDS
    def cmd_confirm(self):
        pass

    def cmd_cancel(self):
        pass

    def cmd_move(self, delta: Tuple[int, int]) -> None:
        pass
    # endregion

    # region UI COMMANDS
    def ui_set_player_name(self, name: str) -> None:
        self.character_info["name"] = name

    def ui_continue(self):
        self.client.session.world.create_prefab("Player", {
            "position": {
                "x": 0, "y": 0
            },
            "renderable": {
                "char": "@",
                "fg": (255, 255, 255)
            },
            "moniker": {
                "name": self.character_info["name"]
            }
        }, uid = "PLAYER")

        self.client.push_screen(Stage(self.client))

    def ui_cancel(self):
        self.client.pop_screen()
    # endregion
