from __future__ import annotations
from typing import TYPE_CHECKING, Optional

import logging
import tcod

from anathema.screen import ScreenManager
import anathema.prepare as prepare
from anathema.console import console
from anathema.screens.main_menu import MainMenu
from anathema.commander import Commander
from anathema.engine.engine import EngineLoop

if TYPE_CHECKING:
    from anathema.session import Session

logger = logging.getLogger(__file__)


class Client(ScreenManager):
    """Client class for the entire application.
    Inherits the base ScreenManager and handles the screen loop.
    """

    context: tcod.context.Context

    def __init__(self) -> None:
        super().__init__()
        self.commander: Commander = Commander(self)
        self.loop: Optional[EngineLoop] = None
        self.session: Optional[Session] = None
        self.main_menu = MainMenu(self)

    def initialize(self, session: Session) -> None:
        self.loop = EngineLoop(self, session)
        self.session = session
        self.replace_screen(self.main_menu)

    def teardown(self):
        pass

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
