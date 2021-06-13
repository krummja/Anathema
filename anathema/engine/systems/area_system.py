from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from anathema.engine.systems.base_system import BaseSystem

if TYPE_CHECKING:
    from anathema.engine.engine import EngineLoop
    from ecstremity import Query, World


class AreaSystem(BaseSystem):

    _needs_update: bool = True
    current_area = None

    def initialize(self):
        self.query("current", all_of=[ "EnvIsCurrent" ])

    def update(self):
        if self._needs_update:
            self.current_area = self.queries["current"].result[0]
            self._needs_update = False

    def needs_update(self) -> None:
        self._needs_update = True
