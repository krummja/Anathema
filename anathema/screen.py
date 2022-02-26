from __future__ import annotations
from typing import TYPE_CHECKING, List, Any

import logging

from anathema import prepare
from anathema.views import FirstResponderContainerView
from anathema.lib.morphism import Size

if TYPE_CHECKING:
    from anathema.client import Client
    from anathema.view import View
    from tcod.event import KeyboardEvent, TextInput


logger = logging.getLogger(__name__)


def add_input_handler(screen: Screen, handler: View) -> None:
    if not getattr(handler, "handle_input"):
        raise ValueError("Invalid handler")
    screen.input_handlers.append(handler)


def remove_input_handler(screen: Screen, handler: View) -> None:
    screen.input_handlers.remove(handler)


class Screen:
    """Prototype class for Screens.

    All screens should inherit from this. No direct instances of this class
    should be created.
    """

    def __init__(self, client: Client, views: List[View]) -> None:
        self.client = client

        if not isinstance(views, list):
            views = [views]  # type: ignore

        self._input_handlers: List[View] = []

        self.view = FirstResponderContainerView(subviews=views, screen=self)
        add_input_handler(self, self.view)

        self.start_time: float = 0.0
        self.current_time: float = 0.0
        self.covers_screen: bool = True

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def input_handlers(self) -> List[View]:
        """
        A list of :py:class:`View` objects that are sub-views capable
        of handling input.
        """
        return self._input_handlers

    def handle_textinput(self, event: TextInput) -> None:
        for handler in self._input_handlers:
            handler.handle_textinput(event)

    def handle_input(self, event: KeyboardEvent) -> None:
        """
        Pass a :py:class:`KeyboardEvent` to the sub-views registered
        as valid input handlers to this :py:class:`Screen`.
        """
        for handler in self._input_handlers:
            handler.handle_input(event)

    def on_enter(self, *args: List[Any]) -> None:
        """Lifecycle hook run when the Screen becomes active."""
        pass

    def on_leave(self, *args: List[Any]) -> None:
        """Lifecycle hook run when the Screen is resigned as active."""
        pass

    def become_active(self) -> None:
        """Lifecycle hook for initial setup of the screen on becoming active."""
        pass

    def resign_active(self) -> None:
        """Lifecycle hook for cleanup of the screen on resigning as active."""
        pass

    def pre_update(self) -> None:
        """Timing hook that runs just before the screen update step."""
        pass

    def on_update(self, _is_active: bool = False) -> bool:
        """Timing hook that runs during the update step.

        In general, do not override this method.
        """
        self.pre_update()
        self.view.frame = self.view.frame.with_size(
            Size(*prepare.CONSOLE_SIZE)
        )
        self.view.perform_layout()
        self.view.perform_draw()
        self.post_update()
        return True

    def post_update(self) -> None:
        """Timing hook that runs just after the screen update step."""
        pass
