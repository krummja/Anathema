from __future__ import annotations
from typing import *
from anathema.lib.morphism import *
from dataclasses import dataclass
from .generation import PlanetGenerator, PlanetView

if TYPE_CHECKING:
    from anathema.lib.ecstremity import Entity
    from anathema.engine.engine import EngineLoop
    from anathema.typedefs import Color
    from anathema.data.components.envtilemap import TileData


class WorldManager:

    def __init__(self, loop: EngineLoop) -> None:
        self.world = loop.world
        self.generator = PlanetGenerator(200, 100)
        self.viewer = PlanetView(self.generator)
