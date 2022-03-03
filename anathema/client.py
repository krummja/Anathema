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
from anathema.gui import TestScreen
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
        
        test_screen = TestScreen(self)
        test_screen.add_view_class(TestView)
        test_screen.add_view_class(TestView2)
        test_screen.add_view(TextField(
            screen = test_screen,
            point = Point(42, 30),
            text = "Testing the TextField view!",
            fg = (255, 0, 255)
        ))
        test_screen.add_view(Button(
            screen = test_screen,
            point = Point(42, 35),
            text = "Test Button",
        ))
        test_screen.add_view(Button(
            screen = test_screen,
            point = Point(42, 38),
            text = "Test Button",
        ))
        self.screens.replace_screen(test_screen)

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
