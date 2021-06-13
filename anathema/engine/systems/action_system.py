from __future__ import annotations
from collections import deque
from anathema.engine.systems.base_system import BaseSystem


class ActionSystem(BaseSystem):

    def initialize(self):
        self.query("actors", all_of = [ "Actor" ])
        self.query("area", all_of = [ "EnvTilemap", "EnvIsCurrent" ])

    def update(self):
        entities = self.queries["actors"].result
        # current_area = self.queries["area"].result[0]

        sorted_entities = deque(sorted(entities, key=(lambda e: e["Actor"]), reverse = True))
        entity = sorted_entities[0]

        if entity and not entity["Actor"].has_energy:
            self.loop.clock.increment(-1 * entity["Actor"].energy)
            for entity in entities:
                entity["Actor"].add_energy(self.loop.clock.tick_delta)

        while entity and entity["Actor"].has_energy:

            if entity.has("IsPlayer"):
                action = self.loop.player.get_next_action()
                if action:
                    action()
                return True

            entity.fire_event("take_action")
            if len(entities) > 0:
                entity = sorted_entities.popleft()

        return False
