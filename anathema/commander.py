from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Optional,
    Any,
    Generic,
    TypeVar,
    Callable
)

import tcod

if TYPE_CHECKING:
    from tcod.event import TextInput, KeyDown
    from anathema.client import Client
    from anathema.view import View
    from anathema.screen import Screen
    from anathema.input.command_set import CommandSet


T = TypeVar("T")


class Commander(tcod.event.EventDispatch[Any]):

    def __init__(self, client: Client) -> None:
        self.client = client
        self._commands: Dict[str, Dict[int, str]] = {
            'MainMenu': {
                tcod.event.K_RETURN: "confirm",
                tcod.event.K_ESCAPE: "cancel"
            },
            'Stage': {},
        }

    def ev_textinput(self, event: TextInput) -> None:
        if self.client.active_screen:
            self.client.active_screen.handle_textinput(event)

    def ev_keydown(self, event: KeyDown) -> Any:
        if self.client.active_screen:
            self.client.active_screen.handle_input(event)

            command_set = self._commands[self.client.active_screen.name]
            if event.sym in command_set:
                try:
                    func = getattr(self.client.active_screen, f"cmd_{command_set[event.sym]}")
                    return func()
                except AttributeError:
                    pass

    def update(self) -> Optional[Any]:
        for event in tcod.event.get():
            value = self.dispatch(event)
            if value is not None:
                return value
        return None
