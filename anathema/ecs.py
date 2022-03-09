from __future__ import annotations

import json
import logging
import os
from typing import TYPE_CHECKING

from anathema.constants.paths import PREFABS
from anathema.data.components import components
from anathema.lib.ecstremity import Engine
from anathema.log import bcolors, cprint

if TYPE_CHECKING:
    from ecstremity import World


logger = logging.getLogger(__file__)


engine = Engine()


def load_components(engine: Engine) -> None:
    logger.info(cprint(bcolors.OKBLUE, "Registering Component definitions:"))
    for component in components:
        logger.info(cprint(bcolors.OKBLUE, f"     Loaded Component {component.comp_id}"))
        engine.register_component(component)


def load_prefabs_from_json(engine: Engine) -> None:
    logger.info(cprint(bcolors.OKBLUE, "Registering Prefab definitions:"))
    prefabs = [f for f in os.listdir(PREFABS) if f.endswith(".json")]
    definitions = []
    for prefab in prefabs:
        with open(PREFABS + prefab) as json_def:
            definition = json.load(json_def)
            definitions.append(definition)
    definitions.sort(key = (lambda definition: len(definition["inherit"])))
    for definition in definitions:
        logger.info(cprint(bcolors.OKBLUE, f"     Loaded Prefab {definition['name']}"))
        engine.prefabs.register(definition)


def load_prefabs_from_xml(engine: Engine) -> None:
    prefabs = []


def new_world() -> World:
    return engine.create_world()
