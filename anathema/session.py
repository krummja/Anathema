from __future__ import annotations

import datetime
import json
import logging
import os
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from anathema import ecs
from anathema.constants import paths
from anathema.prepare import SAVE_METHOD

if TYPE_CHECKING:
    from anathema.lib.ecstremity import World

logger = logging.getLogger(__name__)


TIME_FORMAT = "%Y_%m_%d %H%M%S"
SAVE_PATH = paths.USER_GAME_SAVE_DIR


def list_save_files() -> Optional[List[str]]:
    """Return a list of save files in the user game save directory."""
    save_files: List[str] = [file for file in os.listdir(paths.USER_GAME_SAVE_DIR)]
    if save_files:
        return save_files
    return None


def setup_session(session: Session) -> Session:
    """Set up a Session object from a save, or simply return a new one."""
    save_files = list_save_files()
    if save_files is not None:
        last_saved = save_files[-1]
        session_data = open_save_file(os.path.join(paths.USER_GAME_SAVE_DIR, last_saved))
        session = session.restore(session_data)
    return session


# SESSION -> DATA DICT
def serialize_session_data(session: Session) -> Dict[str, Any]:
    """Get Session state dict, write new time info and return."""
    save_data: Dict[str, Any] = session.serialize()
    return save_data


def write_to_file(save_data: Dict[str, Any]) -> None:
    """Write Session data dict to JSON format and save to file."""
    save_data["time"] = datetime.datetime.now().strftime(TIME_FORMAT)
    save_data["name"] = save_data["time"]
    file_name: str = save_data["name"] + ".save"

    if SAVE_METHOD == "CBOR":
        text = cbor.dumps(save_data)
    else:
        text = json.dumps(save_data, indent=4, separators=(",", ": "))

    with open(os.path.join(SAVE_PATH, file_name), "w") as f:
        logger.info(f"Saving data to save file: {SAVE_PATH}/{file_name}")
        f.write(text)
        f.close()


def open_save_file(save_data: str) -> Optional[Any]:
    """Unpack data from the save path and return it."""
    try:
        with open(save_data) as save_file:
            try:
                return json.load(save_file)
            except ValueError:
                logger.error(f"Cannot decode save JSON: {save_data}")
            try:
                return cbor.load(save_file)
            except ValueError:
                logger.error(f"Cannot decode save CBOR: {save_data}")
            return {}
    except OSError as e:
        logger.info(e)
        return None


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

    @classmethod
    def restore(cls, session_data: Dict[str, Any]) -> Session:
        """Constructor. Deserialize save data and create a Session object."""
        world = ecs.new_world()
        world.deserialize(session_data["world"])
        date_time = session_data["time"]
        session = cls(world, date_time)
        return session

    def save(self):
        save_data = serialize_session_data(self)
        write_to_file(save_data)

    def serialize(self) -> Dict[str, Any]:
        """Serialize ECS Data and return as a dict."""
        return {
            "name": "",
            "time": "",
            "world": self.world.serialize(),
        }
