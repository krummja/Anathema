from __future__ import annotations
from typing import Dict, Any, TYPE_CHECKING

import datetime

import ecstremity

from anathema import ecs
from anathema import storage

if TYPE_CHECKING:
    from ecstremity import World, Entity
    from anathema.client import Client


TIME_FORMAT = "%Y/%m/%d %H:%M:%S"


class Session:
    """Holds references to the current game session's persistent data.
    Sessionable data is handled by ecstremity's serialization methods.
    """

    def __init__(self, world: World, date_time: str) -> None:
        self.world = world
        self.date_time = date_time

    @classmethod
    def new(cls) -> Session:
        world = ecs.new_world()
        date_time = datetime.datetime.now().strftime(TIME_FORMAT)
        session = cls(world, date_time)
        return session

    # @classmethod
    # def restore(cls, session_data: Dict[str, Any]) -> Session:
    #     """Constructor. Deserialize save data and create a Session object."""
    #     world = ecs.new_world()
    #     world.deserialize(session_data["world"])
    #     # player = world.deserialize_entity(session_data["player"])
    #     date_time = session_data["time"]
    #
    #     session = cls(world, date_time)
    #     return session

    def save(self):
        save_data = storage.get_save_data(self)
        storage.write_to_file(save_data)

    def serialize(self) -> Dict[str, Any]:
        """Serialize ECS Data and return as a dict."""
        return {
            "name": "",
            "time": "",
            "world": self.world.serialize(),
        }
