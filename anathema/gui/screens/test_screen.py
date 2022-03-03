from __future__ import annotations
from typing import *

from gui.screen import Screen
from anathema.gui.views.button import Button
from anathema.gui.views.text_field import TextField
from anathema.gui.views.test_view import TestView2
from anathema.gui.views.alignment import Snap
from anathema.lib.morphism import *

if TYPE_CHECKING:
    from anathema.client import Client


class TestScreen(Screen):
    
    def __init__(self, client: Client) -> None:
        super().__init__(client)
        test_view = TestView2(self)
        self.add_view(test_view)
        Snap.to_bottom_left(test_view)

        self.add_view(TextField(
            screen = self,
            point = Point(42, 30),
            text = "Testing the TextField view!",
            fg = (255, 0, 255)
        ))
        self.add_view(Button(
            screen = self,
            point = Point(42, 35),
            text = "Test Button",
        ))
        self.add_view(Button(
            screen = self,
            point = Point(42, 38),
            text = "Test Button",
            callback = self.client.quit
        ))

    def cmd_quit(self) -> None:
        self.client.quit()
