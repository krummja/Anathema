from __future__ import annotations
from typing import TYPE_CHECKING

import logging
import tcod


from anathema.screen import ScreenManager
import anathema.prepare as prepare
from anathema.console import console
from anathema.screens.main_menu import MainMenu
from anathema.commander import Commander

logger = logging.getLogger(__file__)


class Client(ScreenManager):
    """Client class for the entire application.
    Inherits the base ScreenManager and handles the game loop.
    """

    context: tcod.context.Context

    def __init__(self) -> None:
        super().__init__()
        self.commander: Commander = Commander(self)

    def initialize(self) -> None:
        self.replace_screen(MainMenu(self))

    def main(self) -> None:
        with tcod.context.new(
            columns=prepare.CONSOLE_SIZE[0],
            rows=prepare.CONSOLE_SIZE[1],
            tileset=prepare.TILESET,
            title="Anathema",
            renderer=tcod.RENDERER_SDL2,
            vsync=prepare.VSYNC,
        ) as self.context:
            while self.should_continue:
                self.update()
                self.commander.update()
                self.context.present(console.root)

    def update(self) -> None:
        i = 0
        for j, screen in enumerate(self._stack):
            if screen.covers_screen:
                i = j
        for screen in self._stack[i:]:
            screen.on_update(screen == self._stack[-1])
