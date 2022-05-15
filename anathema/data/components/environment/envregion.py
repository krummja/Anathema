from __future__ import annotations
from typing import *

from anathema.lib.ecstremity import *

if TYPE_CHECKING:
    pass


class EnvRegion(Component):

    def __init__(self, world_id: str, region_id: str) -> None:
        self.world_id = world_id
        self.region_id = region_id
