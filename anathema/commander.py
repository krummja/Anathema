from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Tuple,
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
                tcod.event.K_ESCAPE: "cancel",
            },
            "CharacterCreation": {
                tcod.event.K_RETURN: "confirm",
                tcod.event.K_ESCAPE: "cancel",
            },
            'Stage': {
                tcod.event.K_RETURN: "confirm",
                tcod.event.K_ESCAPE: "cancel",
            },
        }
        self._move_keys: Dict[int, Tuple[int, int]] = {
            # Arrow keys.
            tcod.event.K_LEFT    : (-1, 0),
            tcod.event.K_RIGHT   : (1, 0),
            tcod.event.K_UP      : (0, -1),
            tcod.event.K_DOWN    : (0, 1),
            tcod.event.K_HOME    : (-1, -1),
            tcod.event.K_END     : (-1, 1),
            tcod.event.K_PAGEUP  : (1, -1),
            tcod.event.K_PAGEDOWN: (1, 1),
            # Numpad keys.
            tcod.event.K_KP_1    : (-1, 1),
            tcod.event.K_KP_2    : (0, 1),
            tcod.event.K_KP_3    : (1, 1),
            tcod.event.K_KP_4    : (-1, 0),
            tcod.event.K_KP_6    : (1, 0),
            tcod.event.K_KP_7    : (-1, -1),
            tcod.event.K_KP_8    : (0, -1),
            tcod.event.K_KP_9    : (1, -1),
        }

    def ev_textinput(self, event: TextInput) -> None:
        if self.client.active_screen:
            self.client.active_screen.handle_textinput(event)

    def ev_keydown(self, event: KeyDown) -> Any:
        if self.client.active_screen:
            command_set = self._commands[self.client.active_screen.name]

            self.client.active_screen.handle_input(event)

            if event.sym in command_set:
                try:
                    func = getattr(self.client.active_screen, f"cmd_{command_set[event.sym]}")
                    return func()
                except AttributeError:
                    pass

            elif event.sym in self._move_keys:
                try:
                    func = getattr(self.client.active_screen, "cmd_move")
                    return func(self._move_keys[event.sym])
                except AttributeError:
                    pass

    def update(self) -> Optional[Any]:
        for event in tcod.event.get():
            value = self.dispatch(event)
            if value:
                return value
        return None
