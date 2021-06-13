from __future__ import annotations
from typing import TYPE_CHECKING, Tuple
from collections import deque

if TYPE_CHECKING:
    from ecstremity import Entity
    from anathema.engine.engine import EngineLoop


class Player:

    def __init__(self, loop: EngineLoop) -> None:
        self.loop = loop
        self._uid = "PLAYER"
        self._action_queue = deque([])

    @property
    def entity(self) -> Entity:
        return self.loop.world.get_entity(self._uid)

    @property
    def uid(self) -> str:
        return self._uid

    @uid.setter
    def uid(self, value: str) -> None:
        self._uid = value

    @property
    def position(self):
        return self.entity["Position"].xy

    def get_next_action(self):
        try:
            return self._action_queue.popleft()
        except IndexError:
            pass

    def queue_action(self, action):
        self._action_queue.append(action)

    def move(self, direction: Tuple[int, int]) -> None:
        target_x = self.position[0] + direction[0]
        target_y = self.position[1] + direction[1]
        self.queue_action((lambda: self.entity.fire_event(
            "try_move", {"target": (target_x, target_y)}
        )))

    def wait(self, turns: int = 1) -> None:
        self.queue_action((lambda: self.entity.fire_event(
            "energy_consumed", {"cost": turns * 1000}
        )))
