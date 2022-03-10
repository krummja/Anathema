from __future__ import annotations
from typing import *
from random import randint
from dataclasses import dataclass

if TYPE_CHECKING:
    from anathema.lib.ecstremity import Entity


@dataclass
class Attribute:
    name: str
    abbreviation: str


ATTR_MIG = Attribute("might", "MIG")
ATTR_FIN = Attribute("finesse", "FIN")
ATTR_VIT = Attribute("vitality", "VIT")
ATTR_PIE = Attribute("piety", "PIE")
ATTR_CUN = Attribute("cunning", "CUN")
ATTR_KNO = Attribute("knowledge", "KNO")


def get_attribute_name(attribute: Attribute) -> str:
    return attribute.name


def get_attribute_abbr(attribute: Attribute) -> str:
    return attribute.abbreviation


def get_attribute(attribute: Attribute, entity: Entity) -> int:
    return entity["Attributes"][attribute.name]


def roll_attribute(attribute: Attribute, entity: Entity) -> int:
    roll = randint(1, 20)
    return roll + get_attribute(attribute, entity)


def attribute_check(attribute: Attribute, entity: Entity, target: int) -> bool:
    return roll_attribute(attribute, entity) >= target
