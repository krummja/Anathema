from __future__ import annotations
from typing import TYPE_CHECKING

from anathema.lib.ecstremity import Component
from anathema.engine.message import Message

if TYPE_CHECKING:
    from anathema.lib.ecstremity import EntityEvent


class Legs(Component):

    def __init__(self, leg_count: int = 2) -> None:
        self.leg_count = leg_count

    def on_try_move(self, evt: EntityEvent) -> None:
        if self.client.loop.area_system.current_area["EnvTilemap"].is_blocked(*evt.data.target):
            evt.data.report = ("The way is blocked!", (255, 0, 0))
            self.entity.fire_event("report", evt.data)
        else:
            cost = (20 / (20 + 20)) * 1000
            evt.data.cost = cost
            evt.data.report = ("Step!", (255, 0, 255))
            self.entity.fire_event("energy_consumed", evt.data)
            self.entity.fire_event("report", evt.data)
            self.update_position(*evt.data.target)
            evt.handle()

    def update_position(self, x: int, y: int) -> None:
        self.entity["Position"].xy = x, y
