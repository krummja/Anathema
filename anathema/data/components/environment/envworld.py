from __future__ import annotations
from typing import *

from anathema.lib.ecstremity import *

if TYPE_CHECKING:
    from .envregion import EnvRegion


class EnvWorld(Component):

    def __init__(self, world_id: str) -> None:
        self.world_id = world_id
        self._region_data: Dict[str, Entity] = {}
