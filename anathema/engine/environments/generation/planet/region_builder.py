from __future__ import annotations
from typing import *
from anathema.lib.ecstremity import *

if TYPE_CHECKING:
    from .generator import world_tile
    from anathema.engine.environments.world_manager import WorldManager


class RegionBuilder:

    def __init__(self, world_manager: WorldManager) -> None:
        self.world_manager = world_manager

    def new_region(
            self,
            region_data: world_tile,
            environs: Dict[Tuple[int, int], world_tile]
        ) -> None:
        region_entity = self.world_manager.world.create_entity()

