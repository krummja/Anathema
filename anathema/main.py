"""Module responsible for booting the different parts of the game engine."""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional

import logging

from anathema import log
from anathema import prepare
from anathema.commander import Commander

if TYPE_CHECKING:
    from anathema.screen import Screen

logger = logging.getLogger(__file__)


def main(load_slot: Optional[Screen] = None) -> None:
    """
    Application entrypoint. Sets up the Client instance and starts the
    game loop.
    """

    log.configure()

    from anathema.client import Client
    logger.info("CLIENT: Initializing.")
    client: Client = Client()

    if load_slot:
        logger.info("Save data found.")
        pass

    client.initialize()

    logger.info("CLIENT: Running.")
    client.main()
