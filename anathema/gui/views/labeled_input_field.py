from __future__ import annotations
from typing import *

from gui.screen import Screen
from anathema.gui.view import View
from anathema.gui.views.button import Button
from anathema.gui.views.text_field import TextField
from anathema.gui.views.text_input import TextInputField
from anathema.gui.views.alignment import Snap
from anathema.gui.views.rect_view import RectView
from anathema.gui.views.grid import Grid
from anathema.lib.morphism import *


class LabeledInputField(View):

    def __init__(
            self,
            screen: Screen,
            label: str = "",
            point: Point = Point(0, 0),
            width: int = 0
        ) -> None:
        super().__init__()
        self.screen = screen
        self.label = label
        self._bounds = Rect(point, Size(width + len(label), 3))

        self._frame = RectView()
        self._frame.bounds = self._bounds

        _x = point.x
        _y = point.y
        self._text_field = TextInputField(
            point = point + Point(1, 1) + Point(len(label), 0),
            size = Size(width - 2, 1)
        )

        self._label_field = TextField(label, point = point + Point(1, 1))

        screen.add_view(self._frame)
        screen.add_view(self._text_field)
        screen.add_view(self._label_field)

    def perform_draw(self) -> None:
        if self._frame.screen is None:
            self._frame.screen = self.screen
        self._frame.perform_draw()
        self._label_field.perform_draw()
        self._text_field.perform_draw()

    def handle_textinput(self, event: TextInput) -> bool:
        return self._text_field.handle_textinput(event)

