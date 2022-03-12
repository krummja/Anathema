
from __future__ import annotations
from typing import *

import random
from anathema.engine.behavior.goal_types.bored_goal_type import BoredGoalType

if TYPE_CHECKING:
    from anathema.client import Client
    from anathema.lib.ecstremity import *


def pick_name():
    names = [
        "Korok Shyden",
        "Eithne",
        "Rolm",
        "Gloisur",
        "Braagen",
        "Sethchell",
        "Kiroum",
        "Darglin",
        "Hiabaid Akoorb",
        "Naadra",
        "Jethrik",
        "Zynx",
        "Datz",
        "Batrosque",
        "Eriptil",
        "Gleyden",
        "Frosserthil",
        "Ancelyn Helziatz",
        "Mekeesha",
    ]
    return names[random.randrange(0, len(names)-1)]


def create_spawnable(client: Client):
    def spawn(x: int, y: int):
        wanderer = client.loop.world.create_prefab("Wanderer", {
            "position": {
                "x": x,
                "y": y,
            },
            "renderable": {
                "char": "T",
                "fg": (0, 255, 255)
            },
            "noun": {
                "text": pick_name()
            }
        })
        wanderer["Brain"].append_goal(BoredGoalType().create(client.loop.world))
        return wanderer
    return spawn
