from __future__ import annotations

from typing import List, Optional

from anathema.console import console
from gui.screen import Screen
from gui.screens.character_creation import CharacterCreation
from gui.screens.main_menu import MainMenu
from gui.screens.stage import Stage


class ScreenManager:
    """Base ScreenManager.

    This manager is inherited by Anathema's :py:class:`Client`, which
    does the actual work at runtime.
    """

    def __init__(self, client: Client) -> None:
        self._stack: List[Screen] = []
        self.should_continue: bool = True
        self.screens = {
            "main": MainMenu(client),
            "character": CharacterCreation(client),
            "stage": Stage(client)
        }

    @property
    def active_screen(self) -> Optional[Screen]:
        if self._stack:
            return self._stack[-1]
        return None

    def replace_screen(self, screen: Screen | str) -> None:
        if isinstance(screen, str):
            _screen = self.screens[screen]
        else:
            _screen = screen
        if self._stack:
            self.pop_screen(may_exit=False)
        console.clear()
        self.push_screen(_screen)

    def push_screen(self, screen: Screen) -> None:
        self._stack.append(screen)
        screen.on_enter()

    def pop_screen(self, may_exit: bool = False) -> None:
        if self.active_screen:
            self.active_screen.resign_active()
        if self._stack:
            last_screen = self._stack.pop()
            last_screen.on_leave()
        if self.active_screen:
            self.active_screen.become_active()
        elif may_exit:
            self.should_continue = False

    def pop_to_first_screen(self) -> None:
        while len(self._stack) > 1:
            self.pop_screen()

    def update(self) -> None:
        i = 0
        for j, screen in enumerate(self._stack):
            if screen.covers_screen:
                i = j
        for screen in self._stack[i:]:
            screen.on_update(screen == self._stack[-1])

    def on_quit(self) -> None:
        print("Exiting...")
        while self._stack:
            self.pop_screen(may_exit=True)
