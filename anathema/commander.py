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
from enum import Enum, auto

import tcod

if TYPE_CHECKING:
    from anathema.client import Client
    from anathema.view import View
    from anathema.input.command_set import CommandSet


T = TypeVar("T")


class Domain(Enum):
    DEFAULT = auto()
    MAIN_MENU = auto()
    STAGE = auto()


class Commander(tcod.event.EventDispatch[Any]):

    def __init__(self, client: Client) -> None:
        self.client = client
        self._commands: Dict[str, CommandSet] = {}

    def commands_for(self, key: str) -> CommandSet:
        return self._commands[key]

    def update(self) -> Optional[Any]:
        for event in tcod.event.get():
            value = self.dispatch(event)
            if value is not None:
                return value
        return None

    def ev_textinput(self, event: tcod.event.TextInput) -> None:
        if self.client.active_screen is not None:
            self.client.active_screen.handle_textinput(event)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Any:
        if self.client.active_screen is not None:
            self.client.active_screen.handle_input(event)

            command_set = self._commands[self.client.active_screen.name]
            if event.sym in command_set.commands:
                try:
                    return command_set.execute(event.sym)
                except AttributeError:
                    pass

    def register(self, command_set: CommandSet) -> None:
        self._commands[command_set.name] = command_set
