from __future__ import annotations
from typing import TYPE_CHECKING

from ecstremity import Component

if TYPE_CHECKING:
    from ecstremity import EntityEvent


class Legs(Component):

    def __init__(self, leg_count: int = 2) -> None:
        self.leg_count = leg_count

    def on_try_move(self, evt: EntityEvent) -> None:
        pass

    def update_position(self, x: int, y: int) -> None:
        pass
