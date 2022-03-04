from __future__ import annotations
from typing import *

from gui.screen import Screen
from anathema.gui.views.button import Button
from anathema.gui.views.text_field import TextField
from anathema.gui.views.test_view import TestView2
from anathema.gui.views.alignment import Snap
from anathema.gui.views.group import VerticalGroup, HorizontalGroup
from anathema.gui.views.rect_view import RectView
from anathema.gui.views.grid import Grid
from anathema.lib.morphism import *

if TYPE_CHECKING:
    from anathema.client import Client


class Stage(Screen):
    
    def __init__(self, client: Client) -> None:
        super().__init__(client)

        self.add_view(Grid(rows = 10, cols = 10))

        # bottom_pane = RectView(size = Size(-1, 5))
        # self.add_view(bottom_pane)
        # Snap(bottom_pane).bottom()
        #
        # left_pane = RectView(size = Size(20, -1))
        # self.add_view(left_pane)
        # Snap(left_pane).left()
        #
        # right_pane = RectView(size = Size(26, -1))
        # self.add_view(right_pane)
        # Snap(right_pane).right()

    def cmd_quit(self) -> None:
        self.client.screens.pop_screen()
