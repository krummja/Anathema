from __future__ import annotations
from typing import TYPE_CHECKING, List, Tuple

from morphism import (Rect, Size, Point)  # type: ignore

import tcod
from anathema.screen import Screen
from anathema.views.layout import Layout
from anathema.views.button_view import ButtonView
from anathema.views.rect_view import RectView
from anathema.views.label_view import LabelView
from anathema.prepare import CONSOLE_SIZE

if TYPE_CHECKING:
    from anathema.client import Client
    from anathema.view import View


POSITION_RECT = Rect(Point(0, 0), Size(*CONSOLE_SIZE))


class MainMenu(Screen):

    def __init__(self, client: Client) -> None:

        # region LOGO
        self.logo_rect = RectView(
            layout = Layout(
                bottom=POSITION_RECT.relative_point(1.0, 0.33)[1]))
        # endregion

        # region MAIN MENU
        self.start_button = ButtonView(
            "Start",
            callback = self.ui_start,
            align_horz = "left",
            align_vert = "bottom",
            layout = Layout(bottom = 8, left = 2))

        self.new_button = ButtonView(
            "Quit",
            callback = self.ui_quit,
            align_horz = "left",
            align_vert = "bottom",
            layout = Layout(bottom = 6, left = 2))

        self.button_box = RectView(
            layout = Layout(
                top = POSITION_RECT.relative_point(1.0, 0.66)[1] + 1,
                right = POSITION_RECT.relative_point(0.66, 1.0)[0] + 1),
            subviews = [self.start_button, self.new_button])
        # endregion

        self.views: List[View] = [self.logo_rect, self.button_box]
        super().__init__(client=client, views=self.views)

    # region UI COMMANDS
    def ui_start(self) -> None:
        print("Start!")

    def ui_quit(self) -> None:
        self.client.quit()
    # endregion

    # region SCREEN COMMANDS
    def cmd_confirm(self):
        pass

    def cmd_cancel(self):
        pass

    def cmd_move(self, delta: Tuple[int, int]) -> None:
        pass
    # endregion
