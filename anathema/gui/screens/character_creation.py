from __future__ import annotations
from typing import *

from anathema.lib.morphism import *
from gui.screen import Screen
from anathema.gui.screens.stage import Stage
from anathema.gui.views import *
from anathema.console import console


if TYPE_CHECKING:
    from anathema.client import Client


class CharacterCreation(Screen):
    
    def __init__(self, client: Client) -> None:
        super().__init__(client)

        test = LabeledInputField(self, label = "Test: ", point = Point(5, 5), width = 20)
        self.add_view(test)
        Snap(test).top(20).left(20)

        continue_button = Button("Continue", callback = self.ui_continue, framed = False)
        self.add_view(continue_button)
        Snap(continue_button).bottom(6).left(5)

    def ui_continue(self) -> None:
        self.client.session.world.create_prefab("Player", {
            "position": {
                "x": 0, "y": 0
            },
            "renderable": {
                "char": "@",
                "fg": (255, 255, 255)
            },
            "moniker": {
                "name": "Test Player"
            },
            "noun": {
                "text": "Test Player"
            }
        }, uid = "PLAYER")
        self.client.screens.replace_screen(Stage(self.client))

    def cmd_quit(self) -> None:
        self.client.screens.replace_screen("main")
