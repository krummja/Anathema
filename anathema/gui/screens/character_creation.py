from __future__ import annotations
from typing import *

from anathema.lib.morphism import *
from gui.screen import Screen
from anathema.gui.views import *


if TYPE_CHECKING:
    from anathema.client import Client


class CharacterCreation(Screen):
    
    def __init__(self, client: Client) -> None:
        super().__init__(client)

        test = LabeledInputField(self, label = "Test: ", point = Point(5, 5), width = 30)
        self.add_view(test)
        Snap(test).top(20).left(20)

    def cmd_quit(self) -> None:
        self.client.screens.pop_screen()
