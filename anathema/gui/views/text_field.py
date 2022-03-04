from __future__ import annotations
from typing import *

from anathema.gui.view import View
from anathema.lib.morphism import *

if TYPE_CHECKING:
    from anathema.typedefs import Color
    from anathema.gui.screen import Screen


class TextField(View):

    def __init__(
            self,
            text: str,
            point: Point = Point(0, 0),
            fg: Optional[Color] = None,
            bg: Optional[Color] = None,
        ) -> None:
        super().__init__()
        self.point = point
        self.text = text
        self.fg = fg if fg else (255, 255, 255)
        self.bg = bg if bg else (21, 21, 21)
        self._bounds = Rect(self.point, Size(len(self.text), 1))

    @property
    def bounds(self) -> Rect:
        return self._bounds

    @bounds.setter
    def bounds(self, value: Rect) -> None:
        new_pos = value.point
        self._bounds = Rect(new_pos, self.bounds.size)

    def perform_draw(self) -> None:
        self.screen.console.print(self.bounds.point, self.text, self.fg, self.bg)
