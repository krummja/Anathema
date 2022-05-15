from __future__ import annotations
from typing import *

from anathema.lib.ecstremity import *

if TYPE_CHECKING:
    pass


class EnvArea(Component):

    def __init__(self, world_id: str, region_id: str, area_id: str) -> None:
        self.world_id = world_id
        self.region_id = region_id
        self.area_id = area_id
