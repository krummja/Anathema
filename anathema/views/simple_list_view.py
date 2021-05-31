from __future__ import annotations
from typing import Optional, View, TYPE_CHECKING

from anathema.view import View
from anathema.views.rect_view import RectView
from anathema.views.label_view import LabelView

if TYPE_CHECKING:
    from morphism import Rect  # type: ignore


class SimpleListView(View):

    def __init__(
            self,
            # Superclass parameters.
            screen: Optional[Screen] = None,
            layout: Optional[Layout] = None,
            subviews: Optional[List[View]] = None,
            frame: Optional[Rect] = None
        ) -> None:
        self.rect_view: RectView = RectView()
        self.rect_view.fill = False

        self.list_items: List[LabelView] = []
        super().__init__(screen, layout, subviews, frame)

    @property
    def inner_height(self) -> int:
        return self.frame.height - 3

    def update(self, display_list: List[LabelView]) -> None:
        self.list_items.clear()
        self.list_items = [LabelView(item, align_horz = "left") for item in display_list]
