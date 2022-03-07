from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from anathema.engine.engine import EngineLoop


class WorldManager:

    def __init__(self, loop: EngineLoop) -> None:
        self.loop = loop
        self.generator = None

