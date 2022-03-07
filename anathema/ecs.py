from __future__ import annotations
from typing import TYPE_CHECKING
import os
import json
import importlib
import logging

from anathema.log import bcolors, cprint

from anathema.data import components
from anathema.lib.ecstremity import Engine
from anathema.constants.paths import COMPONENTS, PREFABS

if TYPE_CHECKING:
    from ecstremity import World


engine = Engine()


logger = logging.getLogger(__file__)


def load_components(engine: Engine) -> None:
    from anathema.data.components import components
    for component in components:
        logger.info(cprint(bcolors.OKBLUE, f"   Loaded Component {component.comp_id}"))
        engine.register_component(component)


def load_prefabs(engine: Engine) -> None:
    prefabs = [f for f in os.listdir(PREFABS) if f.endswith(".json")]
    definitions = []
    for prefab in prefabs:
        with open(PREFABS + prefab) as json_def:
            definition = json.load(json_def)
            definitions.append(definition)
    definitions.sort(key = (lambda definition: len(definition["inherit"])))
    for definition in definitions:
        logger.info(cprint(bcolors.OKBLUE, f"   Loaded Prefab {definition['name']}"))
        engine.prefabs.register(definition)


def new_world() -> World:
    return engine.create_world()
