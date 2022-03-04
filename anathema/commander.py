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
from xml.dom.minidom import Attr

import tcod

if TYPE_CHECKING:
    from tcod.event import TextInput, KeyDown
    from anathema.client import Client


T = TypeVar("T")


class Commander(tcod.event.EventDispatch[Any]):

    def __init__(self, client: Client) -> None:
        self.client = client
        self._commands: Dict[str, Dict[int, str]] = {
            'MainMenu': {
                tcod.event.K_ESCAPE: "quit"
            },
            'Stage': {
                tcod.event.K_ESCAPE: "quit"
            }
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
        if self.client.screens.active_screen:
            self.client.screens.active_screen.handle_textinput(event)

    def ev_keydown(self, event: KeyDown) -> Any:
        if self.client.screens.active_screen:
            screen = self.client.screens.active_screen
            command_set = self._commands[screen.name]
            self.client.screens.active_screen.handle_input(event)
            if event.sym in command_set:
                try:
                    func = getattr(screen, f"cmd_{command_set[event.sym]}")
                    return func()
                except AttributeError as e:
                    print(e)
            elif event.sym in self._move_keys:
                try:
                    func = getattr(self.client.screens.active_screen, "cmd_move")
                    return func(self._move_keys[event.sym])
                except AttributeError:
                    pass

    def update(self) -> Optional[Any]:
        for event in tcod.event.get():
            value = self.dispatch(event)
            if value:
                return value
        return None
