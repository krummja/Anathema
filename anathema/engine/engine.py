from __future__ import annotations
from typing import TYPE_CHECKING
import time

from anathema.ecs import engine
from anathema.console import console

from anathema.engine.camera import Camera
from anathema.engine.renderer import Renderer
from anathema.engine.clock import Clock
from anathema.engine.player import Player

from anathema.engine.systems.action_system import ActionSystem
from anathema.engine.systems.render_system import RenderSystem
from anathema.engine.systems.fov_system import FOVSystem
from anathema.engine.systems.area_system import AreaSystem

if TYPE_CHECKING:
    from anathema.session import Session
    from anathema.client import Client


class EngineLoop:

    def __init__(self, client: Client, session: Session) -> None:
        """Core engine class.
        Handles the actual game modules and runs the game loop.
        """
        self.is_running = False
        self.client = client
        self.session = session
        self.world = session.world

        self.camera = Camera(self)
        self.renderer = Renderer(self)
        self.clock = Clock(self)
        self.player = Player(self)

        self.area_system = AreaSystem(self)
        self.action_system = ActionSystem(self)
        self.fov_system = FOVSystem(self)
        self.render_system = RenderSystem(self)
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
