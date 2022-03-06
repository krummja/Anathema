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
            title: Optional[str] = None
        ) -> None:
        super().__init__()
        self.title = title
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
        self._bounds = value

    def perform_draw(self) -> None:
        self.screen.console.draw_frame(self.bounds, fg=self.fg, bg=self.bg)
        if self.title is not None:
            _title = f"┤ {self.title} ├"
            _point = Point(self.bounds.point.x + 2, self.bounds.point.y)
            self.screen.console.print(_point, _title, self.fg, self.bg)
