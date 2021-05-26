from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List

from ecstremity import Engine  # type: ignore
from anathema.engine.components import all_components

if TYPE_CHECKING:
    from ecstremity import World


engine = Engine()
for component in all_components():
    engine.register_component(component)


def new_world() -> World:
    return engine.create_world()


default_world: World = new_world()
