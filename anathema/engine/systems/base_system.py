from __future__ import annotations

from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from anathema.engine.engine import EngineLoop
    from ecstremity import Query, World


class BaseSystem:

    def __init__(self, loop: EngineLoop) -> None:
        self.loop = loop
        self.ecs = loop.ecs
        self.queries: Dict[str, Query] = {}
        self.initialize()

    def query(self, key: str, all_of=None, any_of=None, none_of=None) -> None:
        self.queries[key] = self.loop.world.create_query(all_of, any_of, none_of)

    def initialize(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError
