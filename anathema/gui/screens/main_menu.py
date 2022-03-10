from __future__ import annotations
from typing import *

from gui.screen import Screen
from anathema.gui.screens.character_creation import CharacterCreation

from anathema.gui.views import *
from anathema.lib.morphism import *
from anathema.console import console

if TYPE_CHECKING:
    from anathema.client import Client


class MainMenu(Screen):
    
    def __init__(self, client: Client) -> None:
        super().__init__(client)

        logo = Logo()
        self.add_view(logo)
        Snap(logo).top().center()

        # Start button
        start_button = Button("Start", callback = self.start, framed = False)
        self.add_view(start_button)
        Snap(start_button).bottom(8).left(5)

        # Quit button
        quit_button = Button("Quit", callback = client.quit, framed = False)
        self.add_view(quit_button)
        Snap(quit_button).bottom(4).left(5)

        # Help text
        help_str = ""
        help_str += "[↑]/[↓]  Prev/Next Item  "
        help_str += "[←]/[→]  Prev/Next Group  "
        help_str += "[ENTER] Confirm  "
        help_text = TextField(help_str, fg = (100, 100, 100))
        self.add_view(help_text)
        Snap(help_text).bottom(1).center()

        self.load_menu = RectView(size = Size(30, 40))

    def start(self) -> None:
        # TODO Separate this out into a world generation sequence
        area = self.client.loop.world.create_prefab("ForestArea", {
            "EnvTilemap": {
                "width": 120,
                "height": 120
            },
            "EnvTerrain": {}
        }, uid = "TEST_AREA")

        area.add("EnvIsCurrent", {})
        area["EnvTilemap"].setup_terrain()

        self.client.loop.initialize()
        self.client.screens.replace_screen("character")

    def new(self) -> None:
        pass

    def cmd_open(self) -> None:
        self.add_view(self.load_menu)
        Snap(self.load_menu).center()

    def cmd_close(self) -> None:
        self.remove_view(self.load_menu)

    def cmd_quit(self) -> None:
        self.client.quit()

    def cmd_move(self, direction: Tuple[int, int]) -> None:
        if direction == (0, 1):
            self.find_next_responder()
        elif direction == (0, -1):
            self.find_prev_responder()
        elif direction == (1, 0):
            self.find_next_group()
        elif direction == (-1, 0):
            self.find_previous_group()
