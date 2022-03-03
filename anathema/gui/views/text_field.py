from __future__ import annotations
from typing import *

from anathema.gui.view import View
from anathema.lib.morphism import Point

if TYPE_CHECKING:
    from anathema.typedefs import Color
    from anathema.gui.screen import Screen


class TextField(View):

    def __init__(
            self,
            screen: Screen,
            point: Point,
            text: str,
            fg: Optional[Color] = None,
            bg: Optional[Color] = None,
        ) -> None:
        super().__init__(screen)
        self.point = point
        self.text = text
        self.fg = fg if fg else (255, 255, 255)
        self.bg = bg if bg else (21, 21, 21)

    def perform_draw(self) -> None:
        self.screen.console.print(self.point, self.text, self.fg, self.bg)
