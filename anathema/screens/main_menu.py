from __future__ import annotations
from typing import TYPE_CHECKING, List

from morphism import (Rect, Size, Point)  # type: ignore

from anathema.screen import Screen
from anathema.views.layout import Layout
from anathema.views.button_view import ButtonView
from anathema.views.rect_view import RectView
from anathema.views.label_view import LabelView
from anathema.prepare import CONSOLE_SIZE

if TYPE_CHECKING:
    import anathema.client
    from anathema.views.view import View


POSITION_RECT = Rect(Point(0, 0), Size(*CONSOLE_SIZE))


class MainMenu(Screen):

    def __init__(self, client: anathema.client.Client) -> None:

        self.start_button = ButtonView(
            "Start", callback = (lambda: print("Start!")),
            align_horz = "left", align_vert = "bottom",
            layout = Layout(bottom = 8, left = 2))
        self.new_button = ButtonView(
            "New", callback = (lambda: print("New!")),
            align_horz = "left", align_vert = "bottom",
            layout = Layout(bottom = 6, left = 2))

        self.button_box = RectView(
            layout = Layout(top = POSITION_RECT.relative_point(1.0, 0.66)[1] + 1,
                            right = POSITION_RECT.relative_point(0.66, 1.0)[0] + 1),
            subviews = [self.start_button, self.new_button]
        )

        self.test_label = LabelView(
            text="Test Label",
            layout = Layout.row_bottom(0.1)
        )

        self.logo_rect = RectView(
            layout = Layout(bottom=POSITION_RECT.relative_point(1.0, 0.33)[1]),
            subviews = [self.test_label]
        )

        self.views: List[View] = [self.logo_rect, self.button_box]
        super().__init__(client=client, views=self.views)

    def pre_update(self) -> None:
        self.test_label.update("Test Label")
