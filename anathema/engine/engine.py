from __future__ import annotations

import logging
from typing import *
import time

from anathema.ecs import engine
from anathema.console import console

from anathema.engine.camera import Camera
from anathema.engine.renderer import Renderer
from anathema.engine.clock import Clock
from anathema.engine.player import Player
from anathema.engine.messenger import Messenger
from anathema.engine.environments.world_manager import WorldManager

from anathema.engine.systems.action_system import ActionSystem
from anathema.engine.systems.render_system import RenderSystem
from anathema.engine.systems.fov_system import FOVSystem
from anathema.engine.systems.area_system import AreaSystem
from anathema.engine.message import Message
from anathema import log
from anathema.print_utils import cprint, bcolors

if TYPE_CHECKING:
    from anathema.typedefs import Color
    from anathema.client import Client
    from anathema.data.components.noun import Noun
    from anathema.lib.ecstremity.world import World


logger = logging.getLogger(__file__)


class IEngine:

    def __init__(self, client: Client, world: World) -> None:
        self.is_running: bool = False
        self.client = client
        self.world = world

        self.camera = None
        self.renderer = None
        self.clock = None
        self.player = None
        self.messenger = None
        self.world_manager = None

        self.area_system = None
        self.action_system = None
        self.fov_system = None
        self.render_system = None
        self.interaction_system = None
        self.path_system = None

    def initialize(self):
        raise NotImplementedError

    def teardown(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def report(self, message: Message) -> None:
        raise NotImplementedError


class EngineLoop(IEngine):

    def __init__(self, client: Client, world: World) -> None:
        """Core engine class.
        Handles the actual game modules and runs the game loop.
        """
        super().__init__(client, world)

    def initialize(self):
        self.camera = Camera(self)
        self.renderer = Renderer(self)
        self.clock = Clock(self)
        self.player = Player(self)
        self.messenger = Messenger(self)
        self.world_manager = WorldManager(self)

        self.area_system = AreaSystem(self)
        self.action_system = ActionSystem(self)
        self.fov_system = FOVSystem(self)
        self.render_system = RenderSystem(self)
        self.interaction_system = None
        self.path_system = None

        self.is_running = True

    def teardown(self):
        self.is_running = False

        self.camera = None
        self.renderer = None
        self.clock = None
        self.player = None

        self.area_system = None
        self.action_system = None
        self.fov_system = None
        self.render_system = None
        self.interaction_system = None
        self.path_system = None

    @property
    def console(self):
        return console

    @property
    def ecs(self):
        return engine

    def update(self) -> None:
        if self.is_running:

            self.area_system.update()

            for _ in range(20):
                self.clock.update()
                player_turn = self.action_system.update()

                # self.path_system.update()

                if player_turn:
                    self.fov_system.update()
                    self.render_system.update()
                    return

    def report(self, message: Message) -> None:
        logger.info(cprint(bcolors.OKGREEN, message.text))
        self.messenger.add_message(message)
