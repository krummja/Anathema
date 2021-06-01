"""Module responsible for booting the different parts of the game engine."""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import logging

from anathema import log
from anathema import prepare
from anathema.commander import Commander
from anathema.ecs import load_prefabs, load_components, engine
from anathema.session import new_session, load_session

if TYPE_CHECKING:
    from anathema.session import Session
    from anathema.screen import Screen

logger = logging.getLogger(__file__)


def main(load_slot: int) -> None:
    """Application entrypoint. Sets up the Client instance and starts the
    game loop.
    """
    log.configure()

    logger.info("ECS: Registering Component definitions.")
    load_components(engine)

    logger.info("ECS: Registering Prefab definitions.")
    load_prefabs(engine)

    logger.info("CLIENT: Initializing.")
    from anathema.client import Client
    client: Client = Client()

    if load_slot:
        logger.info("Save data found.")
        # FIXME
        session: Session = new_session(load_slot)
    else:
        logger.info("No save data found.")
        logger.info(f"Creating new game session in slot {load_slot}")
        session: Session = new_session(0)

    logger.info("CLIENT: Running.")
    client.initialize(session)
    client.main()
