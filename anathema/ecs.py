from __future__ import annotations
from typing import TYPE_CHECKING
import os
import json
import importlib

from anathema.data import components

from ecstremity import Engine  # type: ignore
from anathema.constants.paths import COMPONENTS, PREFABS

if TYPE_CHECKING:
    from ecstremity import World


engine = Engine()


def load_components(engine: Engine) -> None:
    from anathema.data.components import components
    for component in components:
        engine.register_component(component)


def load_prefabs(engine: Engine) -> None:
    prefabs = [f for f in os.listdir(PREFABS) if f.endswith(".json")]
    for prefab in prefabs:
        with open(PREFABS + prefab) as json_def:
            definition = json.load(json_def)
            engine.prefabs.register(definition)


def new_world() -> World:
    return engine.create_world()
