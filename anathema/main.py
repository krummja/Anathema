from __future__ import annotations
from typing import TYPE_CHECKING, Optional

import logging

from anathema import log
from anathema import prepare

if TYPE_CHECKING:
    from anathema.state import State

logger = logging.getLogger(__name__)


def main(load_slot: Optional[State] = None) -> None:
    log.configure()
    prepare.init()
    config = prepare.CONFIG

    from anathema.client import Client
    client: Client = Client()

    if load_slot:
        pass

    client.main()
