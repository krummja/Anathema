from __future__ import annotations
from typing import *

from gui.screen import Screen
from anathema.gui.views.button import Button
from anathema.gui.views.text_field import TextField
from anathema.gui.views.test_view import TestView2
from anathema.gui.views.alignment import Snap
from anathema.gui.views.group import VerticalGroup, HorizontalGroup
from anathema.lib.morphism import *

if TYPE_CHECKING:
    from anathema.client import Client


class Stage(Screen):
    
    def __init__(self, client: Client) -> None:
        super().__init__(client)
        self.add_view(TextField(Point(10, 10), "Test"))

    def cmd_quit(self) -> None:
        self.client.screens.pop_screen()
