"""Module responsible for booting the different parts of the game engine."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from anathema import log
from anathema.ecs import engine, load_components, load_prefabs_from_json
from anathema.print_utils import bcolors, cprint

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__file__)


def start() -> None:
    """Application entrypoint.
    Sets up the Client instance and starts the game loop.
    """

    # Configure the log.
    log.configure()

    # Import the Client and create a new instance.
    from anathema.client import Client
    client: Client = Client()
    engine.client = client

    # Load ECS stuff.
    load_components(engine)
    load_prefabs_from_json(engine)
    client.initialize(engine.create_world())

    # Let 'er rip!
    client.main()
