from __future__ import annotations
from typing import *

from anathema.lib.ecstremity import Component
from anathema.engine.message import Message

if TYPE_CHECKING:
    from anathema.lib.ecstremity import EntityEvent


class Legs(Component):

    def __init__(self, leg_count: int = 2) -> None:
        self.leg_count = leg_count

    def on_try_move(self, evt: EntityEvent) -> None:
        # TODO At this step, retrieve the entity or tile that is occupying the target tile.
        if self.client.loop.area_system.current_area["EnvTilemap"].is_blocked(*evt.data.target):
            # evt.data.report = Message(f"{0} block[s] your path!", noun1 = self.entity["Noun"], color = (255, 0, 0))
            evt.data.report = Message("Your way is blocked!", color=(255, 0, 0))
            self.entity.fire_event("report", evt.data)
        else:
            cost = (20 / (20 + 20)) * 1000
            evt.data.cost = cost
            self.entity.fire_event("energy_consumed", evt.data)
            self.update_position(*evt.data.target)
            evt.handle()

    def update_position(self, x: int, y: int) -> None:
        self.entity["Position"].xy = x, y
