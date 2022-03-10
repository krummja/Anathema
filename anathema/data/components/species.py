from __future__ import annotations
from typing import *

from anathema.lib.ecstremity import Component
from anathema.data.species import get_species_data

if TYPE_CHECKING:
    from anathema.lib.ecstremity import EntityEvent
    from anathema.data.attributes import Attribute
    from anathema.data.species_data import SpeciesData


class Species(Component):

    def __init__(self, key: str) -> None:
        self.key = key

    @property
    def data(self):
        return get_species_data(self.key)

    @property
    def name(self):
        return self.data.name

    def get_modifier(self, attribute: str):
        return self.data[attribute]

    def on_query_attr_mod(self, evt: EntityEvent):
        mod = self.get_modifier(evt.data.attribute)
        if mod != 0:
            evt.data.modifiers.append((self.name, mod))
