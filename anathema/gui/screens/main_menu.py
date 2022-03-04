from __future__ import annotations
from typing import *

from gui.screen import Screen
from anathema.gui.screens.stage import Stage
from anathema.gui.views.button import Button
from anathema.gui.views.text_field import TextField
from anathema.gui.views.test_view import TestView2
from anathema.gui.views.alignment import Snap
from anathema.gui.views.group import VerticalGroup, HorizontalGroup
from anathema.lib.morphism import *

if TYPE_CHECKING:
    from anathema.client import Client


class MainMenu(Screen):
    
    def __init__(self, client: Client) -> None:
        super().__init__(client)

        buttons = [
                Button("Start", framed = False, callback = self.start),
                Button("Options", framed = False),
                Button("Quit", framed = False, callback = self.client.quit),
            ]
        menu_items = VerticalGroup(self, buttons, padding = 3)
        self.add_view(menu_items)
        Snap(menu_items).bottom().left()

    def start(self) -> None:
        self.client.screens.push_screen(Stage(self.client))

    def cmd_quit(self) -> None:
        self.client.quit()
