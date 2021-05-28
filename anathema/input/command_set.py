from __future__ import annotations
from typing import Dict, List, Optional, Callable, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from anathema.screen import Screen


class Command:

    def __init__(self, key: int) -> None:
        self.key = key
        self._set: Optional[CommandSet] = None

    @property
    def command_set(self) -> Optional[CommandSet]:
        return self._set

    @command_set.setter
    def command_set(self, value: CommandSet) -> None:
        self._set = value

    def func(self) -> None:
        raise NotImplementedError("Command function must be implemented!")


class CommandSet:

    def __init__(self, screen: Screen) -> None:
        self.screen = screen
        self.commands: Dict[int, Command] = {}

    @property
    def name(self) -> str:
        return self.screen.name

    def register(self, command: Command) -> None:
        self.commands[command.key] = command
        command.command_set = self

    def execute(self, sym: int) -> None:
        command = self.commands[sym]
        if command is not None:
            command.func()
