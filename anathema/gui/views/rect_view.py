from __future__ import annotations
from typing import *

from anathema.gui.view import View
from anathema.lib.morphism import *
from anathema.prepare import CONSOLE_SIZE

if TYPE_CHECKING:
    from anathema.typedefs import Color
    from anathema.gui.screen import Screen


class RectView(View):

    def __init__(
            self,
            point: Point = Point(0, 0),
            size: Size = Size(*CONSOLE_SIZE),
            fg: Optional[Color] = None,
            bg: Optional[Color] = None,
        ) -> None:
        super().__init__()
        if size.width == -1:
            size = Size(CONSOLE_SIZE[0], size.height)
        if size.height == -1:
            size = Size(size.width, CONSOLE_SIZE[1])
        self.fg = fg if fg else (255, 255, 255)
        self.bg = bg if bg else (21, 21, 21)
        self._bounds = Rect(point, size)

    @property
    def bounds(self) -> Rect:
        return self._bounds

    @bounds.setter
    def bounds(self, value: Rect) -> None:
        new_pos = value.point
        self._bounds = Rect(new_pos, self.bounds.size)

    def perform_draw(self) -> None:
        self.screen.console.draw_frame(self.bounds, fg=self.fg, bg=self.bg)
