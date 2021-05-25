"""Module responsible for booting the different parts of the game engine."""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional

import logging

from anathema import log
from anathema import prepare

if TYPE_CHECKING:
    from anathema.screen import Screen

logger = logging.getLogger(__file__)


def main(load_slot: Optional[Screen] = None) -> None:
    log.configure()

    logger.info("PREPARE: Initializing.")
    prepare.init()

    logger.info("PREPARE: Loading configuration.")
    config = prepare.CONFIG

    from anathema.client import Client
    logger.info("CLIENT: Initializing.")
    client: Client = Client()

    if load_slot:
        logger.info("Save data found.")
        pass

    logger.info("CLIENT: Running.")
    client.main()
