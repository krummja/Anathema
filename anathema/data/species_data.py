from __future__ import annotations
from typing import *
from dataclasses import dataclass

if TYPE_CHECKING:
    from anathema.data.attributes import Attribute


@dataclass
class SpeciesData:
    name: str = ""
    speed: int = 1
    base_might: int = 10
    base_finesse: int = 10
    base_vitality: int = 10
    base_piety: int = 10
    base_cunning: int = 10
    base_knowledge: int = 10

    def __getitem__(self, key: str) -> Attribute:
        return getattr(self, "base_" + key.name)
