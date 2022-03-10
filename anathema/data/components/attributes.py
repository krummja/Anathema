from __future__ import annotations
from typing import *
from functools import reduce

from anathema.lib.ecstremity import Component
from anathema.data.attributes import ATTR_MIG, ATTR_FIN, ATTR_VIT, ATTR_PIE, ATTR_CUN, ATTR_KNO, get_attribute_name

if TYPE_CHECKING:
    from anathema.data.attributes import *


def sum_modifiers(modifiers):
    _result = reduce(lambda _sum, _cur: _sum + _cur.mod, modifiers)
    return _result


class Attributes(Component):

    def __init__(
            self,
            base_might: int,
            base_finesse: int,
            base_vitality: int,
            base_piety: int,
            base_cunning: int,
            base_knowledge: int
        ) -> None:
        self.base_might = base_might
        self.base_finesse = base_finesse
        self.base_vitality = base_vitality
        self.base_piety = base_piety
        self.base_cunning = base_cunning
        self.base_knowledge = base_knowledge

    def get_attribute_modifiers(self, attribute: Attribute):
        evt = self.entity.fire_event("query_attr_mod", {
            "name": get_attribute_name(attribute),
            "attribute": attribute,
            "modifiers": []
        })
        return evt.data.modifiers

    def get_attribute_modifier_sum(self, attribute: Attribute):
        mods = self.get_attribute_modifiers(attribute)
        return sum_modifiers(mods)

    def data(self, attribute: Attribute) -> Dict[str, Any]:
        base = getattr(self, f"base_{attribute.name}")
        modifiers = self.get_attribute_modifiers(attribute)
        mod_sum = sum_modifiers(modifiers)
        return {
            "attribute": attribute,
            "name": get_attribute_name(attribute),
            "abbreviation": get_attribute_abbr(attribute),
            "modifiers": modifiers,
            "base": base,
            "mod_sum": mod_sum,
            "sum": base + mod_sum
        }

    def get_all(self):
        return {
            "might": self.data(ATTR_MIG),
            "finesse": self.data(ATTR_FIN),
            "vitality": self.data(ATTR_VIT),
            "piety": self.data(ATTR_PIE),
            "cunning": self.data(ATTR_CUN),
            "knowledge": self.data(ATTR_KNO),
        }

    def might(self):
        mod = self.get_attribute_modifier_sum(ATTR_MIG)
        return self.base_might + mod[1]

    def finesse(self):
        mod = self.get_attribute_modifier_sum(ATTR_FIN)
        return self.base_finesse + mod[1]

    def vitality(self):
        mod = self.get_attribute_modifier_sum(ATTR_VIT)
        return self.base_vitality + mod[1]

    def piety(self):
        mod = self.get_attribute_modifier_sum(ATTR_PIE)
        return self.base_piety + mod[1]

    def cunning(self):
        mod = self.get_attribute_modifier_sum(ATTR_CUN)
        return self.base_cunning + mod[1]

    def knowledge(self):
        mod = self.get_attribute_modifier_sum(ATTR_KNO)
        return self.base_knowledge + mod[1]

    def __getitem__(self, key: str):
        if key in ["might", "finesse", "vitality", "piety", "cunning", "knowledge"]:
            attribute = getattr(self, key)
            return attribute()
