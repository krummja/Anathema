from __future__ import annotations
from typing import *

from gui.screen import Screen
from anathema.gui.views import *
from anathema.lib.morphism import *
from anathema.console import console

from anathema.engine.world.planet.generator import Generator

if TYPE_CHECKING:
    from anathema.client import Client


class WorldCreation(Screen):

    def __init__(self, client: Client) -> None:
        super().__init__(client)

