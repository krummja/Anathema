from __future__ import annotations

from typing import *

import tcod
from anathema.console import console
from anathema.gui.view import View
from anathema.lib.morphism import *

if TYPE_CHECKING:
    from anathema.typedefs import Color
    from anathema.gui.screen import Screen


class Button(View):

    def __init__(
            self,
            screen: Screen,
            point: Point,
            text: str,
            framed: bool = True,
            filled: bool = False,
            fg: Color = (255, 255, 255),
            bg: Color = (21, 21, 21),
            sel: Color = (0xde, 0x9c, 0x21),
            callback: Callable[..., Optional[Any]] = (lambda: print("Not implemented!"))
        ) -> None:
        super().__init__(screen, handler = True)
        self.point = point
        self.text = text
        self.framed = framed
        self.filled = filled
        self.fg = self._fg_cached = fg
        self.bg = self._bg_cached = bg
        self.sel = sel
        self.callback = callback

    @property
    def bounds(self) -> Rect:
        point = Point(self.point.x - 1, self.point.y - 1)
        size = Size(len(self.text) + 2, 3)
        return Rect(point, size)

    @property
    def can_become_responder(self) -> bool:
        return True

    @property
    def can_resign_responder(self) -> bool:
        return True

    def on_become_responder(self) -> None:
        self.fg = self.sel

    def on_resign_responder(self) -> None:
        self.fg = self._fg_cached

    def handle_input(self, event: KeyboardEvent) -> bool:
        if self.callback and event.sym == tcod.event.K_RETURN:
            self.callback()
            return True
        return False

    def perform_draw(self) -> None:
        if self.framed:
            console.draw_frame(
                self.bounds,
                fg=(255, 255, 255),
                bg=(21, 21, 21))
        self.screen.console.print(self.point, self.text, self.fg, self.bg)
