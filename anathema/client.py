from __future__ import annotations
from typing import TYPE_CHECKING, Optional

import logging
import tcod

from anathema.lib.morphism import *

from screen_manager import ScreenManager
import anathema.prepare as prepare
from anathema.console import console
from anathema.commander import Commander
from anathema.engine.engine import EngineLoop
from anathema.gui.screens.test_screen import TestScreen
from anathema.gui.screens.main_menu import MainMenu
from anathema.gui.views.text_field import TextField
from anathema.gui.views.button import Button

from anathema.gui.views.test_view import TestView, TestView2

if TYPE_CHECKING:
    from anathema.session import Session
    from tcod.event import KeyboardEvent
    from tcod.console import Console

logger = logging.getLogger(__file__)


class Client:
    """Client class for the entire application.
    Inherits the base ScreenManager and handles the screen loop.
    """

    context: tcod.context.Context

    def __init__(self) -> None:
        super().__init__()
        self.screens = ScreenManager()
        self.commander: Commander = Commander(self)
        self.loop: Optional[EngineLoop] = None
        self.session: Optional[Session] = None

    def initialize(self, session: Session) -> None:
        self.loop = EngineLoop(self, session)
        self.session = session
        
        main_menu = MainMenu(self)
        self.screens.replace_screen(main_menu)

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
            while self.screens.should_continue:
                self.screens.update()
                self.commander.update()
                self.context.present(console.root)

    def quit(self) -> None:
        self.screens.on_quit()
