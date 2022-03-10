from __future__ import annotations
from typing import *
from functools import reduce

from anathema.data.attributes import get_attribute

if TYPE_CHECKING:
    from anathema.lib.ecstremity import Entity
    from anathema.data.attributes import Attribute


class Skill:

    def __init__(self, key: str, name: str, base_attribute: Attribute) -> None:
        self.key = key
        self.name = name
        self.base_attribute = base_attribute

    def get_modifiers(self, entity: Entity):
        evt = entity.fire_event("query_skill_mod", {
            "name": self.name,
            "skill": self.key,
            "modifiers": []
        })
        return evt.data.modifiers

    def get_modifier_sum(self, entity: Entity):
        modifiers = self.get_modifiers(entity)
        return reduce(lambda _sum, _cur: _sum + _cur[1], modifiers)

    def compute(self, entity: Entity) -> int:
        base_attr = get_attribute(self.base_attribute, entity)
        attr = base_attr or 0
        modifier = self.get_modifier_sum(entity)
        return attr + modifier[1]
