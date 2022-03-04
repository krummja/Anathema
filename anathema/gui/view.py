from __future__ import annotations
from typing import *
from anathema.lib.morphism import *

if TYPE_CHECKING:
    from gui.screen import Screen
    from tcod.event import KeyboardEvent


class View:
    
    def __init__(self) -> None:
        self.screen: Screen | None = None
        self.is_responder: bool = False
        self._bounds: Rect = Rect(Point(0, 0), Size(0, 0))

    @property
    def bounds(self) -> Rect:
        return self._bounds

    @bounds.setter
    def bounds(self, value: Rect) -> None:
        self._bounds = value

    @property
    def can_become_responder(self) -> bool:
        return False
    
    @property
    def can_resign_responder(self) -> bool:
        return False

    def on_become_responder(self) -> None:
        self.is_responder = True

    def on_resign_responder(self) -> None:
        self.is_responder = False

    def perform_draw(self) -> None:
        pass

    def update(self) -> None:
        pass

    def handle_input(self, event: KeyboardEvent) -> bool:
        return False
