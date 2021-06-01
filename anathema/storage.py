from __future__ import annotations
from typing import Dict, Any, Optional, TYPE_CHECKING

import datetime
import json
import cbor  # type: ignore
import logging

from anathema.prepare import SAVE_PATH, SAVE_METHOD

if TYPE_CHECKING:
    from anathema.session import Session

logger = logging.getLogger(__name__)
slot_number: int = 0

TIME_FORMAT = "%Y-%m-%d %H:%M"


def get_save_data(session: Session) -> Dict[str, Any]:
    save_data: Dict[str, Any] = session.get_state()
    save_data["time"] = datetime.datetime.now().strftime(TIME_FORMAT)
    return save_data


def save(save_data: Dict[str, Any], slot: int) -> None:
    save_path: str = SAVE_PATH + str(slot) + ".save"
    if SAVE_METHOD == "CBOR":
        text = cbor.dumps(save_data)
    else:
        text = json.dumps(save_data, indent=4, separators=(",", ": "))
    with open(save_path, "w") as f:
        logger.info("Saving data to save file: " + save_path)
        f.write(text)
        f.close()


def load(slot: int) -> Optional[Any]:
    save_path = f"{SAVE_PATH}{slot}.save"
    save_data = open_save_file(save_path)
    if not save_data:
        return None
    else:
        return save_data


def open_save_file(save_path: str) -> Optional[Any]:
    try:
        with open(save_path) as save_file:
            try:
                return json.load(save_file)
            except ValueError:
                logger.error("Cannot decode save JSON: %s", save_path)
            try:
                return cbor.load(save_file)
            except ValueError:
                logger.error("Cannot decode save CBOR: %s", save_path)
            return {}
    except OSError as e:
        logger.info(e)
        return None
