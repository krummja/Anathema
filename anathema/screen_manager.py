from __future__ import annotations

from typing import List, Optional

from gui.screen import Screen


class ScreenManager:
    """Base ScreenManager.

    This manager is inherited by Anathema's :py:class:`Client`, which
    does the actual work at runtime.
    """

    def __init__(self) -> None:
        self._stack: List[Screen] = []
        self.should_continue: bool = True

    @property
    def active_screen(self) -> Optional[Screen]:
        if self._stack:
            return self._stack[-1]
        return None

    def replace_screen(self, screen: Screen) -> None:
        if self._stack:
            self.pop_screen(may_exit=False)
        self.push_screen(screen)

    def push_screen(self, screen: Screen) -> None:
        if self.active_screen:
            self.active_screen.resign_active()
        self._stack.append(screen)
        screen.on_enter()

    def pop_screen(self, may_exit: bool = False) -> None:
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
