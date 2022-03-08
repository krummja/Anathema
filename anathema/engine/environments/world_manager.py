from __future__ import annotations
from typing import *
from anathema.lib.morphism import *
from dataclasses import dataclass

if TYPE_CHECKING:
    from anathema.lib.ecstremity import Entity
    from anathema.engine.engine import EngineLoop
    from anathema.typedefs import Color
    from anathema.data.components.envtilemap import TileData


class WorldManager:

    def __init__(self, loop: EngineLoop) -> None:
        self.loop = loop
        self.generator = None

    def define_virtual_entity(self, data: TileData, **kwargs) -> None:
        entity_def = {

        }
        entity_def.update(kwargs)

    def realize_virtual_entity(self, x: int, y: int, data: TileData) -> Entity | None:
        return self.loop.world.create_prefab("Static", {
            "position": {
                "x": x,
                "y": y
            },
            "renderable": {
                "char": data.char,
                "fg": data.fore
            },
            "moniker": {
                "name": data.key
            },
            "noun": {
                "text": data.key
            }
        })
