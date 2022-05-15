from __future__ import annotations
from typing import *

import random
from anathema.lib import rng
from anathema.engine.resource.resource_set import ResourceSet
from .architecture import Architecture

if TYPE_CHECKING:
    from .region import Region


class ArchitecturalStyle:

    styles: ResourceSet[ArchitecturalStyle] = ResourceSet()

    @staticmethod
    def initialize() -> None:
        pass

    @staticmethod
    def pick(depth: int) -> List[ArchitecturalStyle]:
        result: List[ArchitecturalStyle] = []
        count = min(rng.taper(1, 10), 5)
        has_fillable = False

        while not has_fillable or len(result) < count:
            style = ArchitecturalStyle.styles.try_choose(depth)
            if style.can_fill:
                has_fillable = True
            if style not in result:
                result.append(style)
        return result

    def __init__(
            self,
            name: str,
            factory: Callable[[], Architecture],
            decor_theme: str,
            monster_groups: List[str],
            decor_density: float = 0.1,
            monster_density: float = 1.0,
            item_density: float = 1.0,
            can_fill: bool = True
        ) -> None:
        self.name = name
        self.factory = factory
        self.decor_theme = decor_theme
        self.decor_density = decor_density
        self.monster_groups = monster_groups
        self.monster_density = monster_density
        self.item_density = item_density
        self.can_fill = can_fill

    def create(self, architect: Architect, region: Region) -> Architecture:
        architecture = self.factory()
        architecture.bind(self, architect, region)
        return architecture
