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
            text: str,
            point: Point = Point(0, 0),
            framed: bool = True,
            filled: bool = False,
            fg: Color = (255, 255, 255),
            bg: Color = (21, 21, 21),
            sel: Color = (0xde, 0x9c, 0x21),
            group: int = 0,
            callback: Callable[..., Optional[Any]] = (lambda: print("Not implemented!"))
        ) -> None:
        super().__init__()
        self.text = text
        self.framed = framed
        self.filled = filled
        self.fg = self._fg_cached = fg
        self.bg = self._bg_cached = bg
        self.sel = sel
        self.responder_group = group
        self.callback = callback

        _point = Point(point.x, point.y)
        _size = Size(len(self.text) + 2, 3)
        self._bounds = Rect(_point, _size)

    @property
    def bounds(self) -> Rect:
        return self._bounds

    @bounds.setter
    def bounds(self, value: Rect) -> None:
        new_pos = value.point
        self._bounds = Rect(new_pos, self.bounds.size)

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
            x = self.bounds.x - 1
            y = self.bounds.y - 1
            frame = Rect(Point(x, y), self.bounds.size)
            console.draw_frame(
                frame,
                fg=(255, 255, 255),
                bg=(21, 21, 21))
        self.screen.console.print(self.bounds.point, self.text, self.fg, self.bg)
