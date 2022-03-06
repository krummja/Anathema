from __future__ import annotations
from typing import *
from enum import Enum
import math

from collections import defaultdict

from anathema.console import console
import anathema.prepare as prepare
from anathema.lib.morphism import *

if TYPE_CHECKING:
    from anathema.gui.view import View
    from anathema.typedefs import Number
    from anathema.typedefs import FieldDef


class Snap:

    def __init__(self, view: View, container: Optional[Rect] = None) -> None:
        self.view = view
        self.container = container or view.screen.bounds
        self._side: str = ""

    def bottom(self, offset: int = 0) -> Snap:
        self._side = "bottom"
        view_bounds = self.view.bounds
        point = Point(
            view_bounds.x,
            self.container.height - view_bounds.height - offset
        )
        self.view.bounds = Rect(point, view_bounds.size)
        self.view.update()
        return self

    def left(self, offset: int = 0) -> Snap:
        self._side = "left"
        point = Point(0 + offset, self.view.bounds.y)
        self.view.bounds = Rect(point, self.view.bounds.size)
        self.view.update()
        return self

    def top(self, offset: int = 0) -> Snap:
        self._side = "top"
        point = Point(self.view.bounds.x, 0 + offset)
        self.view.bounds = Rect(point, self.view.bounds.size)
        self.view.update()
        return self

    def right(self, offset: int = 0) -> Snap:
        self._side = "right"
        view_bounds = self.view.bounds
        point = Point(
            self.container.width - self.view.bounds.width - offset,
            view_bounds.y
        )
        self.view.bounds = Rect(point, view_bounds.size)
        self.view.update()
        return self

    def center(self) -> None:
        width = self.view.bounds.width
        height = self.view.bounds.height

        if self._side == "top" or self._side == "bottom":
            x = math.floor(self.container.width / 2) - math.floor(width / 2)
            point = Point(x, self.view.bounds.y)
        elif self._side == "left" or self._side == "right":
            y = math.floor(self.container.height / 2) - math.floor(height / 2)
            point = Point(self.view.bounds.x, y)
        else:
            x = math.floor(self.container.width / 2) - math.floor(width / 2)
            y = math.floor(self.container.height / 2) - math.floor(height / 2)
            point = Point(x, y)
        self.view.bounds = Rect(point, self.view.bounds.size)
