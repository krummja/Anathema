from __future__ import annotations
from typing import Dict, Any, TYPE_CHECKING

from anathema.ecs import engine, new_world
from anathema.storage import *

if TYPE_CHECKING:
    from ecstremity import World, Entity
    from anathema.client import Client


class Session:
    """Holds references to the current game session's persistent data.

    Sessionable data is handled by ecstremity's serialization methods.

    :py:class:`ecstremity.world.World` calls its own serialization method.
    This returns a dict containing a JSON object with all current entity data.

    entities = world.serialize()
    entities = {"entities": [
        "uid": <entity uid>,
        "components": {
            k: v for k, v in Component.__dict__.items() if k[0] != "_"
        }
    ]}

    In addition, specific reference to the player's entity is passed in, as
    well as any data relevant to setting up and creating game environments.
    """

    def __init__(
            self,
            world: World,
            player: Entity,
        ) -> None:
        self.world = world
        self.player = player

    @classmethod
    def new_session(cls) -> Session:
        world = new_world()
        player = world.create_prefab("Player", {
            "position": {
                "x": 0,
                "y": 0,
            },
            "renderable": {
                "char": "@",
                "fg": (255, 255, 255)
            }
        }, "PLAYER")

        session = cls(world, player)
        return session

    @classmethod
    def restore_session(cls, session_data: Dict[str, Any]) -> Session:
        world = new_world()
        world.deserialize(session_data["world"])
        player = world.deserialize_entity(session_data["player"])
        session = cls(world, player)
        return session

    def get_state(self) -> Dict[str, Any]:
        return {
            "world": self.world.serialize(),
            "player": self.player.serialize(),
        }


def new_session(slot: int) -> Session:
    session = Session.new_session()
    save(session.get_state(), slot)
    return session


def load_session(slot: int) -> Session:
    session_data = load(slot)
    session = Session.restore_session(session_data)
    return session
