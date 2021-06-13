from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from anathema.engine.systems.base_system import BaseSystem

if TYPE_CHECKING:
    from anathema.engine.engine import EngineLoop
    from ecstremity import Query, World


class AreaSystem(BaseSystem):

    current_area = None

    def initialize(self):
        self.query("current", all_of=[ "EnvIsCurrent" ])
        self.current_area = self.queries["current"].result[0]

    def update(self):
        raise NotImplementedError
