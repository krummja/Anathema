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

    def realize_virtual_entity(self, x: int, y: int, data: TileData) -> Entity | None:
        return self.world.create_prefab("Static", {
            "position": {
                "x": x,
                "y": y
            },
            "renderable": {
                "char": data.char,
                "fg": data.fore
            },
            "noun": {
                "text": data.key
            }
        })
