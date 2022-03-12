from __future__ import annotations
from typing import *

from anathema.data.spawnables import wanderer
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

        self.name_field = LabeledInputField(self, label = "Name: ", point = Point(5, 5), width = 20)
        self.add_view(self.name_field)
        Snap(self.name_field).top(20).left(20)

        continue_button = Button("Continue", callback = self.ui_continue, framed = False)
        self.add_view(continue_button)
        Snap(continue_button).bottom(6).left(5)

    def ui_continue(self) -> None:
        wanderer.create_spawnable(self.client)(12, 12)
        self.client.loop.world.create_prefab("Player", {
            "position": {
                "x": 25, "y": 25
            },
            "renderable": {
                "char": "@",
                "fg": (255, 255, 255)
            },
            "noun": {
                "text": self.name_field.field_value
            },
            "level": {
                "value": 1
            }
        }, uid = "PLAYER")
        self.client.screens.replace_screen(Stage(self.client))

    def cmd_quit(self) -> None:
        self.client.screens.replace_screen("main")
