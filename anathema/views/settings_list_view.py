from __future__ import annotations
from typing import Callable, Any, Optional, Tuple, Union, TYPE_CHECKING
import math
import tcod

from anathema.views.first_responder_container_view import FirstResponderContainerView
from anathema.views.label_view import LabelView
from anathema.views.rect_view import RectView

if TYPE_CHECKING:
    from morphism import Rect  # type: ignore


class SettingsListView(FirstResponderContainerView):

    def __init__(
            self,
            # SettingsListView parameters.
            label_control_pairs: Tuple[str, Callable[..., Any]],
            value_column_width: int = 16,
            # Superclass parameters.
            screen: Optional[Screen] = None,
            layout: Optional[Layout] = None,
            frame: Optional[Rect] = None
        ) -> None:
        self.rect_view: RectView = RectView()
        self.rect_view.fill = False
        self.scroll_indicator_view = LabelView(text="█")
        super().__init__(
            screen=screen,
            layout=layout,
            subviews=[self.rect_view, self.scroll_indicator_view],
            frame=frame)

        self._min_row: int = 0
        self.value_column_width = value_column_width
        self.first_responder_index: int = 0

        self.labels = [LabelView(t, align_horz="left") for t, _ in label_control_pairs]
        self.values = [c for _, c in label_control_pairs]

        self.add_subviews(self.labels)
        self.add_subviews(self.values)
        self.find_next_responder()

    @property
    def can_become_first_responder(self) -> bool:
        return True

    def did_become_first_responder(self) -> None:
        super().did_become_first_responder()
        self.rect_view.style = 'double'

    def did_resign_first_responder(self) -> None:
        super().did_resign_first_responder()
        self.rect_view.style = 'single'

    @property
    def min_row(self) -> int:
        return self._min_row

    @min_row.setter
    def min_row(self, value: int) -> None:
        self._min_row = value
        self.needs_layout = True

    @property
    def inner_height(self) -> int:
        return self.frame.height - 3

    @property
    def scroll_fraction(self) -> Union[float, int]:
        try:
            return self.min_row / (len(self.labels) - self.inner_height - 1)
        except ZeroDivisionError:
            return -1

    def get_is_in_view(self, y: int) -> bool:
        return self.min_row <= y <= self.min_row + self.inner_height

    def scroll_to(self, y: int) -> None:
        if self.inner_height <= 0:
            return
        if y < self.min_row:
            self.min_row = y
        elif y > self.min_row + self.inner_height:
            self.min_row = min(max(0, y - self.inner_height), len(self.labels) - self.inner_height)

    def set_first_responder_in_visible_area(self) -> None:
        if self.first_responder_index and self.get_is_in_view(self.first_responder_index):
            return
        self.first_responder_container_view.set_first_responder(self.values[self.min_row])

    def layout_subviews(self) -> None:
        self.rect_view.apply_springs_and_struts_layout_in_superview()
        if self.scroll_fraction >= 0:
            self.scroll_indicator_view.frame = Rect(
                Point(self.bounds.width - 1, 1 +
                      floor(self.inner_height * self.scroll_fraction)),
                Size(1, 1))

        for i in range(len(self.labels)):
            is_in_view = self.get_is_in_view(i)
            if is_in_view:
                y = 1 + self.bounds.y + i - self.min_row
                self.labels[i].frame = Rect(
                    Point(self.bounds.x + 1, y),
                    Size(self.bounds.width - self.value_column_width - 2, 1))
                self.values[i].frame = Rect(
                    Point(self.bounds.x + 1 + self.bounds.width - self.value_column_width - 2, y),
                    Size(self.value_column_width, 1))
            self.labels[i].is_hidden = not is_in_view
            self.values[i].is_hidden = not is_in_view

    def descendant_did_become_first_responder(self, control: Callable[..., Any]) -> None:
        for i in range(len(self.labels)):
            if self.values[i] == control:
                if not self.get_is_in_view(i):
                    self.first_responder_index = i
                    self.scroll_to(i)
                break

    def descendant_did_resign_first_responder(self, control: Callable[..., Any]) -> None:
        self.first_responder_index = None

    def handle_input_after_first_responder(self, val: tcod.event.KeyDown, can_resign: bool) -> bool:
        if val.sym == tcod.event.K_UP:
            self.find_prev_responder()
            return True

        elif val.sym == tcod.event.K_DOWN:
            self.find_next_responder()
            return True

        elif (val.sym == tcod.event.K_PAGEUP or
              val.sym == tcod.event.K_COMMA & tcod.event.KMOD_LSHIFT):
            self.min_row = max(0, self.min_row - self.inner_height)
            self.set_first_responder_in_visible_area()
            return True

        elif (val.sym == tcod.event.K_PAGEDOWN or
              val.sym == tcod.event.K_PERIOD & tcod.event.KMOD_LSHIFT):
            self.min_row = min(
                len(self.labels) - self.inner_height - 1,
                self.min_row + self.inner_height)
            self.set_first_responder_in_visible_area()
            return True
