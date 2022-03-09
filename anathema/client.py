from __future__ import annotations

import logging
from typing import Optional, TYPE_CHECKING

import tcod

import anathema.prepare as prepare
from anathema.commander import Commander
from anathema.console import console
from anathema.engine.engine import EngineLoop
from screen_manager import ScreenManager
from anathema.print_utils import bcolors, cprint

if TYPE_CHECKING:
    from anathema.lib.ecstremity.world import World

logger = logging.getLogger(__file__)


class Client:
    """Client class for the entire application.
    Inherits the base ScreenManager and handles the screen loop.
    """

    context: tcod.context.Context

    def __init__(self) -> None:
        logger.info(cprint(bcolors.OKBLUE, f"Instancing {self.__class__.__name__}"))
        self.screens = ScreenManager(self)
        self.commander: Commander = Commander(self)
        self.loop: Optional[EngineLoop] = None

    def initialize(self, world: World) -> None:
        self.loop = EngineLoop(self, world)
        self.screens.replace_screen("main")

    def main(self) -> None:
        logger.info(cprint(bcolors.OKBLUE, "Starting main loop"))
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
