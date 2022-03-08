from __future__ import annotations

from typing import *

from anathema.lib.morphism import *

if TYPE_CHECKING:
    from gui.screen import Screen
    from tcod.event import KeyboardEvent, TextInput


class View:
    
    def __init__(self) -> None:
        self.screen: Screen | None = None
        self.is_responder: bool = False
        self.responder_group: int = 0
        self._bounds: Rect = Rect(Point(0, 0), Size(0, 0))

    @property
    def bounds(self) -> Rect:
        """Rect object that defines the position and dimensions of the View."""
        return self._bounds

    @bounds.setter
    def bounds(self, value: Rect) -> None:
        """Set the Rect object that defines the position and dimension of
        the View.

        Customize this in subclasses to have dynamic bounds calculation.
        """
        self._bounds = value

    @property
    def can_become_responder(self) -> bool:
        """Override this to permit a subclass to enter the Responder queue."""
        return False
    
    @property
    def can_resign_responder(self) -> bool:
        """Override this to permit a subclass to exit the Responder queue. """
        return False

    def on_become_responder(self) -> None:
        """Hook invoked when a View becomes an active Responder."""
        self.is_responder = True

    def on_resign_responder(self) -> None:
        """Hook invoked when a View resigns active Responder."""
        self.is_responder = False

    def draw(self) -> None:
        self.perform_draw()

    def perform_draw(self) -> None:
        """Override in subclasses to give the View its appearance in the console."""
        pass

    def handle_input(self, event: KeyboardEvent) -> bool:
        """Override in subclasses to handle inputs from the core input event bus."""
        return False

    def handle_textinput(self, event: TextInput) -> bool:
        return False

    def update(self):
        pass
