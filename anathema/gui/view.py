from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from gui.screen import Screen
    from tcod.event import KeyboardEvent


class View:
    
    def __init__(self, screen: Screen, handler: bool = False) -> None:
        self.is_input_handler = handler
        self.screen = screen
        self.is_responder: bool = False

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

    def handle_input(self, event: KeyboardEvent) -> bool:
        return False
