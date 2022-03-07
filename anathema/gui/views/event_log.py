from __future__ import annotations
from typing import *

import tcod.console

from anathema.lib.morphism import *
from anathema.gui.views import *
from anathema.gui.view import View
from anathema.gui.ui_colors import RESET

if TYPE_CHECKING:
    from anathema.engine.message import Message
    from anathema.typedefs import Color


class EventLog(View):

    def __init__(
            self,
            point: Point,
            size: Size
        ) -> None:
        super().__init__()
        self._bounds = Rect(point, size)

    def perform_draw(self) -> None:
        i: int = 0
        x, y = self.bounds.left + 1, self.bounds.bottom - 2
        log: List[Message] = self.screen.client.loop.log

        # Display the text that has scrolled up beyond the bottom line.
        for msg in log[-2::-1]:
            text = self._format(msg.text, msg.count, msg.color, True)
            i += tcod.console.get_height_rect(self.bounds.width, msg.text)
            if i >= 9:
                break
            self.screen.console.print_box(
                Rect(Point(x, y - i), Size(self.bounds.width, 0)),
                text)

        for msg in log[::1]:
            text = self._format(msg.text, msg.count, msg.color)
            self.screen.console.print_box(
                Rect(Point(x, y), Size(self.bounds.width, 0)),
                text + " " * (self.bounds.width - len(text) - 2))

    def _format(self, text: str, count: int, col: Color, fade: bool = False) -> str:
        # TODO Alright this is extremely messy but it works! Fix it up to be less ugly.
        wht = (255, 255, 255)
        if fade:
            col = (col[0] // 2, col[1] // 2, col[2] // 2)
            wht = (255 // 2, 255 // 2, 255 // 2)
        if count > 1:
            text = f"{tcod.COLCTRL_FORE_RGB:c}{col[0]:c}{col[1]:c}{col[2]:c}{text}{RESET}"\
                   f"{tcod.COLCTRL_FORE_RGB:c}{wht[0]:c}{wht[1]:c}{wht[2]:c}(x{count}){RESET}"
        else:
            text = f"{tcod.COLCTRL_FORE_RGB:c}{col[0]:c}{col[1]:c}{col[2]:c}{text}{RESET}"
        return text
