from __future__ import annotations
from typing import *

import logging

import tcod.event

from anathema.console import console
from anathema.lib.morphism import *
from anathema.prepare import CONSOLE_SIZE

if TYPE_CHECKING:
    from anathema.gui.view import View
    from anathema.client import Client
    from tcod.event import KeyboardEvent, TextInput


logger = logging.getLogger(__name__)


class Screen:
    """Prototype class for Screens.

    All screens should inherit from this. No direct instances of this class
    should be created.
    """

    def __init__(self, client: Client) -> None:
        self.console = console
        self.client = client
        self.views: List[View] = []
        self.covers_screen: bool = True
        self.responders: List[View] = []
        self.responder: Optional[View] = None

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def bounds(self):
        return Rect(Point(0, 0), Size(*CONSOLE_SIZE))

    def add_view_class(self, view: Type[View]) -> None:
        _view = view()
        _view.screen = self
        self.add_view(_view)

    def add_view(self, view: View) -> None:
        if view.screen is None:
            view.screen = self
        self.views.append(view)
        if view.can_become_responder:
            self.responders.append(view)
            self.set_responder(self.responders[0])

    def remove_view(self, view: View) -> None:
        if view not in self.views:
            return
        self.views.remove(view)

    def set_responder(self, value: Optional[View]) -> None:
        if self.responder:
            self.responder.on_resign_responder()
        self.responder = value
        if self.responder:
            self.responder.on_become_responder()

    def find_next_responder(self) -> None:
        existing_responder = self.responder
        if self.responder is None:
            existing_responder = self.responders[0]
        responders = [v for v in self.responders if v.can_become_responder]

        try:
            i = responders.index(existing_responder)
            if i == len(responders) - 1:
                self.set_responder(responders[0])
            else:
                self.set_responder(responders[i + 1])
        except ValueError:
            if responders:
                self.set_responder(responders[0])
            else:
                self.set_responder(None)

    def find_prev_responder(self) -> None:
        existing_responder = self.responder
        if self.responder is None:
            existing_responder = self.responders[0]
        responders = [v for v in self.responders if v.can_become_responder]

        try:
            i = responders.index(existing_responder)
            if i == 0:
                self.set_responder(responders[-1])
            else:
                self.set_responder(responders[i - 1])
        except ValueError:
            if responders:
                self.set_responder(responders[-1])
            else:
                self.set_responder(None)

    def handle_input_after_responder(self, event: KeyboardEvent, can_resign: bool) -> bool:
        if can_resign and event.sym == tcod.event.K_TAB:
            if event.mod & tcod.event.KMOD_LSHIFT:
                self.find_prev_responder()
                return True
            else:
                self.find_next_responder()
                return True
        return False

    def handle_input(self, event: KeyboardEvent) -> bool:
        handled = self.responder and self.responder.handle_input(event)
        if self.responder and not handled:
            for responder in self.responders:
                if responder.handle_input(event):
                    return True
        can_resign = self.responders and self.responder.can_resign_responder
        return self.handle_input_after_responder(event, can_resign)

    def become_active(self) -> None:
        pass

    def resign_active(self) -> None:
        pass

    def on_enter(self, *args: List[Any]) -> None:
        """Lifecycle hook run when the Screen becomes active."""
        pass

    def on_leave(self, *args: List[Any]) -> None:
        """Lifecycle hook run when the Screen is resigned as active."""
        pass

    def pre_update(self) -> None:
        """Timing hook that runs just before the screen update step."""
        pass

    def on_update(self, _is_active: bool = False) -> bool:
        """Timing hook that runs during the update step.

        In general, do not override this method.
        """
        self.pre_update()
        for view in self.views:
            view.perform_draw()
        self.post_update()
        return True

    def post_update(self) -> None:
        """Timing hook that runs just after the screen update step."""
        pass
