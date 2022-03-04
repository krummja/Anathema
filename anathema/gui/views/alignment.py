from __future__ import annotations
from typing import *
import math

from anathema.console import console
import anathema.prepare as prepare
from anathema.lib.morphism import *

if TYPE_CHECKING:
    from anathema.gui.view import View


class Snap:

    def __init__(self, view: View, container: Optional[Rect] = None) -> None:
        self.view = view
        self.container = container or view.screen.bounds
        self._side: str = ""

    def bottom(self) -> Snap:
        self._side = "bottom"
        view_bounds = self.view.bounds
        point = Point(
            view_bounds.x,
            self.container.height - view_bounds.height
        )
        self.view.bounds = Rect(point, view_bounds.size)
        self.view.update()
        return self

    def left(self) -> Snap:
        self._side = "left"
        point = Point(0, self.view.bounds.y)
        self.view.bounds = Rect(point, self.view.bounds.size)
        self.view.update()
        return self

    def top(self) -> Snap:
        self._side = "top"
        point = Point(0, self.view.bounds.y)
        self.view.bounds = Rect(point, self.view.bounds.size)
        self.view.update()
        return self

    def right(self) -> Snap:
        self._side = "right"
        view_bounds = self.view.bounds
        point = Point(
            self.container.width - self.view.bounds.width,
            view_bounds.y
        )
        self.view.bounds = Rect(point, view_bounds.size)
        self.view.update()
        return self

    def center(self) -> None:
        point = Point(0, 0)
        width = self.view.bounds.width
        height = self.view.bounds.height

        if self._side == "top" or self._side == "bottom":
            x = math.floor(self.container.width / 2) - math.floor(width / 2)
            point = Point(x, self.view.bounds.y)
        if self._side == "left" or self._side == "right":
            y = math.floor(self.container.height / 2) - math.floor(height / 2)
            point = Point(self.view.bounds.x, y)

        self.view.bounds = Rect(point, self.view.bounds.size)
