from __future__ import annotations
from typing import *

from time import time
import tcod.event

from anathema.gui.view import View
from anathema.lib.morphism import *
from anathema.console import console
from dataclasses import dataclass

if TYPE_CHECKING:
    from tcod.event import KeyboardEvent, TextInput
    from anathema.typedefs import Color
    from anathema.gui.screen import Screen


@dataclass
class TextInputConfig:
    initial_value: str = ""
    color_unselected_fg = (255, 255, 255)
    color_unselected_bg = (21, 21, 21)
    color_selected_fg = (0xde, 0x9c, 0x21)
    color_selected_bg = (21, 21, 21)


class TextInputField(View):

    def __init__(
            self,
            config: Optional[TextInputConfig] = None,
            callback = (lambda s: print(s)),
            point: Point = Point(0, 0),
            size: Size = Size(0, 0)
        ) -> None:
        super().__init__()
        self.config = config if config is not None else TextInputConfig()
        self.text = self.config.initial_value
        self.callback = callback
        self._bounds: Rect = Rect(point, size)

    @property
    def width(self) -> int:
        return len(self.text) + 1

    def perform_draw(self) -> None:
        fg = self.config.color_selected_fg if self.is_responder else self.config.color_unselected_fg
        bg = self.config.color_selected_bg if self.is_responder else self.config.color_unselected_bg
        console.print(self.bounds.point, self.text, fg = fg, bg = bg)

        text_len = len(self.text)
        text_pos = Point(self.bounds.point.x + text_len, self.bounds.point.y)
        if int(self.bounds.width) > text_len:
            console.print(text_pos, "." * (self.bounds.width - text_len - 1))
        if self.is_responder and int(time() * 1.2) % 2 == 0:
            console.put_char(text_pos, ord("█"))

    @property
    def can_become_responder(self) -> bool:
        return True

    @property
    def can_resign_responder(self) -> bool:
        return True

    def _update_text(self, value: str) -> None:
        self.text = value

    def handle_input(self, event: KeyboardEvent) -> bool:
        if event.sym == tcod.event.K_RETURN:
            self.callback(self.text)
            self.screen.find_next_responder()
            return True
        if event.sym == tcod.event.K_TAB:
            self.callback(self.text)
            return False
        elif event.sym == tcod.event.K_BACKSPACE:
            if self.text:
                self._update_text(self.text[:-1])
                return True

    def handle_textinput(self, event: TextInput) -> bool:
        if self.width < self.bounds.width:
            self._update_text(self.text + event.text)
            return True
        return False
