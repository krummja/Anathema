from __future__ import annotations
from typing import *
from .generation import PlanetGenerator, PlanetView, RegionBuilder

from uuid import uuid1

if TYPE_CHECKING:
    from anathema.lib.ecstremity import Entity
    from anathema.engine.engine import EngineLoop
    from data.components.environment.envtilemap import TileData


class WorldManager:

    def __init__(self, loop: EngineLoop) -> None:
        self.world = loop.world
        self.generator = PlanetGenerator(200, 100)
        self.viewer = PlanetView(self.generator)
        self.region_builder = RegionBuilder(self)
        self._world_uid: str = ""
        self.world_entity: Entity | None = None
        self.regions: Dict[str, Entity] = {}

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

    def create_new_world(self):
        self.world_entity = self.world.create_entity(f"WORLD-{uuid1()}")
        self.world_entity.add("EnvWorld", {"world_id": self.world_entity.uid})

    def add_region(self):
        pass
