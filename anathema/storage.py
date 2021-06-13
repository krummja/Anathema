from __future__ import annotations
from typing import Dict, Any, Optional, TYPE_CHECKING, List

import os
import datetime
import json
import cbor  # type: ignore
import logging

from anathema.constants import paths
from anathema.prepare import SAVE_METHOD

if TYPE_CHECKING:
    from anathema.session import Session

logger = logging.getLogger(__name__)


TIME_FORMAT = "%Y/%m/%d %H:%M:%S"


class SaveTable:

    def __init__(self, slots, characters, times) -> None:
        self.slots = slots
        self.characters = characters
        self.times = times
        self.row_format = "{:>15}"


def list_save_files() -> Optional[List[str]]:
    save_files: List[str] = [file for file in os.listdir(paths.USER_GAME_SAVE_DIR)]
    if save_files:
        return save_files
    return None


# SESSION -> SESSION
def setup_session(session: Session) -> Session:
    save_files = list_save_files()
    if save_files is not None:
        pass  # TODO
    else:
        return session


# SESSION -> DATA DICT
def get_save_data(session: Session) -> Dict[str, Any]:
    """Get Session state dict, write new time info and return."""
    save_data: Dict[str, Any] = session.serialize()
    return save_data


def write_to_file(save_data: Dict[str, Any], slot: int) -> None:
    save_data["time"] = datetime.datetime.now().strftime(TIME_FORMAT)
    save_path: str = SAVE_PATH + str(slot) + ".save"

    if SAVE_METHOD == "CBOR":
        text = cbor.dumps(save_data)
    else:
        text = json.dumps(save_data, indent=4, separators=(",", ": "))

    with open(save_path, "w") as f:
        logger.info(f"Saving data to save file: {save_path}")
        f.write(text)
        f.close()


def load_from_slot(slot: int) -> Optional[Any]:
    """Get a save file based on the slot number and open it."""
    save_file = f"{SAVE_PATH}{slot}.save"
    save_data = open_save_file(save_file)

    if not save_data:
        return None
    else:
        return save_data


def open_save_file(save_path: str) -> Optional[Any]:
    """Unpack data from the save path and return it."""
    try:
        with open(save_path) as save_file:

            try:
                return json.load(save_file)
            except ValueError:
                logger.error(f"Cannot decode save JSON: {save_path}")

            try:
                return cbor.load(save_file)
            except ValueError:
                logger.error(f"Cannot decode save CBOR: {save_path}")

            return {}

    except OSError as e:
        logger.info(e)
        return None
