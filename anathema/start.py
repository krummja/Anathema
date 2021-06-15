"""Module responsible for booting the different parts of the game engine."""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import logging
from anathema.print_utils import bcolors, cprint

from anathema import log
from anathema import storage
from anathema.ecs import load_prefabs, load_components, engine
from anathema.session import Session

if TYPE_CHECKING:
    from anathema.session import Session
    from anathema.screen import Screen

logger = logging.getLogger(__file__)


def start() -> None:
    """Application entrypoint.
    Sets up the Client instance and starts the game loop.
    """

    # Configure the log.
    log.configure()

    # Import the Client and create a new instance.
    logger.info(cprint(bcolors.OKBLUE, "CLIENT: Initializing."))
    from anathema.client import Client

    client: Client = Client()
    engine.client = client

    # Load ECS stuff.
    logger.info(cprint(bcolors.OKBLUE, "ECS: Registering Component definitions."))
    load_components(engine)

    logger.info(cprint(bcolors.OKBLUE, "ECS: Registering Prefab definitions."))
    load_prefabs(engine)

    # Set up Session
    session = Session.new()
    # session = storage.setup_session(session)
    client.initialize(session)

    # Let 'er rip!
    logger.info(cprint(bcolors.OKBLUE, "CLIENT: Running."))
    client.main()
