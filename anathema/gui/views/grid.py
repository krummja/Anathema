from __future__ import annotations
from typing import *

import math
from anathema.gui.view import View
from anathema.lib.morphism import *
from anathema.prepare import CONSOLE_SIZE

if TYPE_CHECKING:
    from anathema.typedefs import Color
    from anathema.gui.screen import Screen


class Grid(View):

    def __init__(
            self,
            rows: int,
            cols: int,
            fg: Optional[Color] = None,
            bg: Optional[Color] = None,
        ) -> None:
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.fg = fg if fg else (255, 255, 255)
        self.bg = bg if bg else (21, 21, 21)
        self._bounds = Rect(Point(0, 0), Size(*CONSOLE_SIZE))

    @property
    def bounds(self) -> Rect:
        return self._bounds

    @bounds.setter
    def bounds(self, value: Rect) -> None:
        new_pos = value.point
        self._bounds = Rect(new_pos, self.bounds.size)

    def perform_draw(self) -> None:
        height = math.floor(CONSOLE_SIZE[0] / self.rows)
        width = math.floor(CONSOLE_SIZE[1] / self.cols)
        i = 0
        for _ in range(0, CONSOLE_SIZE[1]):
            self.screen.console.vline(Point(i, 0), height = CONSOLE_SIZE[1])
            i += width

        j = 0
        for _ in range(0, CONSOLE_SIZE[0]):
            self.screen.console.hline(Point(0, j), width = CONSOLE_SIZE[0])
            j += height
