from __future__ import annotations
from typing import *
from anathema.lib.morphism import *

from anathema.gui.view import View
from anathema.console import console

if TYPE_CHECKING:
    from gui.screen import Screen
    from tcod.event import KeyboardEvent


class VerticalGroup(View):

    def __init__(
            self,
            screen: Screen,
            items: List[View],
            point: Point = Point(0, 0),
            spacing: int = 1,
            padding: int = 1
        ) -> None:
        super().__init__()
        self.items = items
        self.point = point
        self.spacing = spacing
        self.padding = padding

        _point: Point = Point(point.x + padding, point.y + padding)
        self._inner: Rect = Rect(_point, Size(0, 0))

        for item in self.items:
            screen.add_view(item)
        self.compute_item_properties()
        self.compute_bounds()
        self.compute_inner()

    @property
    def inner(self) -> Rect:
        return self._inner

    def compute_bounds(self) -> None:
        width: int = 0
        height: int = 0
        for item in self.items:
            width = max(width, item.bounds.width)
            height += item.bounds.height + self.spacing
        width += (2 * self.padding)
        height += (2 * self.padding)

        self._bounds = Rect(self.point, Size(width, height))

    def compute_item_properties(self) -> None:
        offset = self.inner.point.y
        for item in self.items:
            offset += item.bounds.height + self.spacing
            item.bounds = Rect(Point(self.inner.point.x, offset), item.bounds.size)

    def compute_inner(self):
        self._inner = Rect.from_edges(
            top = self._bounds.top + self.padding,
            bottom = self._bounds.bottom - self.padding - 1,
            left = self._bounds.left + self.padding,
            right = self._bounds.right - self.padding - 1
        )

    def update(self):
        self.compute_inner()
        self.compute_item_properties()


class HorizontalGroup(View):

    def __init__(
            self,
            screen: Screen,
            items: List[View],
            point: Point = Point(0, 0),
            spacing: int = 1,
            padding: int = 1
        ) -> None:
        super().__init__()
        self.items = items
        self.point = point
        self.spacing = spacing
        self.padding = padding

        _point: Point = Point(point.x + padding, point.y + padding)
        self._inner: Rect = Rect(_point, Size(0, 0))

        for item in self.items:
            screen.add_view(item)
        self.compute_item_properties()
        self.compute_bounds()
        self.compute_inner()

    @property
    def inner(self) -> Rect:
        return self._inner

    def compute_bounds(self) -> None:
        width: int = 0
        height: int = 0
        for item in self.items:
            width += max(width, item.bounds.width) + self.spacing
            height = item.bounds.height
        width += (2 * self.padding)
        height += (2 * self.padding)

        self._bounds = Rect(self.point, Size(width, height))

    def compute_item_properties(self) -> None:
        offset = self.inner.point.x
        for item in self.items:
            offset += item.bounds.width + self.spacing
            item.bounds = Rect(Point(offset, self.inner.point.y), item.bounds.size)

    def compute_inner(self):
        self._inner = Rect.from_edges(
            top = self._bounds.top + self.padding,
            bottom = self._bounds.bottom - self.padding - 1,
            left = self._bounds.left + self.padding,
            right = self._bounds.right - self.padding - 1
        )

    def update(self):
        self.compute_inner()
        self.compute_item_properties()
