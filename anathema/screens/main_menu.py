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

        # Main Menu
        self.start_button = ButtonView(
            "Start", callback = (lambda: print("Start!")),
            align_horz = "left", align_vert = "bottom",
            layout = Layout(bottom = 8, left = 2))

        self.new_button = ButtonView(
            "New", callback = (lambda: print("New!")),
            align_horz = "left", align_vert = "bottom",
            layout = Layout(bottom = 6, left = 2))

        self.button_box = RectView(
            layout = Layout(top = POSITION_RECT.relative_point(1.0, 0.66)[1] + 1,
                            right = POSITION_RECT.relative_point(0.66, 1.0)[0] + 1),
            subviews = [self.start_button, self.new_button])

        # Logo Box
        self.logo_rect = RectView(
            layout = Layout(bottom=POSITION_RECT.relative_point(1.0, 0.33)[1]))

        self.views: List[View] = [self.logo_rect, self.button_box]
        super().__init__(client=client, views=self.views)

    def cmd_move(self, delta: Tuple[int, int]) -> None:
        print(delta)
