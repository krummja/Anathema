from __future__ import annotations
from typing import *
from enum import Enum
import math

from anathema.console import console
import anathema.prepare as prepare
from anathema.lib.morphism import *

if TYPE_CHECKING:
    from anathema.gui.view import View
    from anathema.typedefs import Number, FieldDef


class LayoutType(Enum):
    DEFAULT = 1
    FRAME = 2
    INTRINSIC = 3
    CONSTANT = 4
    FRACTION = 5
    UNKNOWN = 6


class Layout:

    def __init__(
            self,
            width: Optional[Number] = None,
            height: Optional[Number] = None,
            top: Optional[Number] = 0,
            right: Optional[Number] = 0,
            bottom: Optional[Number] = 0,
            left: Optional[Number] = 0,
    ) -> None:
        self.width = width
        self.height = height
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    def get_layout_value(self, key: str, view: View) -> Number | Size | None:
        return None

    def get_layout_type(self, key: str) -> LayoutType:
        pass


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

    def layout_in_container(self, layout: Layout) -> None:
        if self.view.parent:
            parent_bounds = self.view.parent.bounds
        else:
            parent_bounds = self.container

        fields: List[FieldDef] = [
            # start   size      end       coord
            ('left', 'width',  'right',  'x'),
            ('top',  'height', 'bottom', 'y'),
        ]

        final_frame = Rect(Point(-1000, -1000), Size(-1000, -1000))

        for (
            field_start,        # LEFT  or  TOP
            field_size,         # WIDTH or  HEIGHT
            field_end,          # RIGHT or  BOTTOM
            field_coord         # X     or  Y
        ) in fields:

            matches = (
                getattr(layout, field_start) is not None,
                getattr(layout, field_size) is not None,
                getattr(layout, field_end) is not None
            )

            if matches == (True, True, True) or matches == (False, False, False):
                # Invalid case
                pass

            elif matches == (True, False, False):
                # START (LEFT or TOP)
                #    final_frame.{field_coord} =
                setattr(final_frame, field_coord, layout.get_layout_value(field_start, self.view))

            elif matches == (True, True, False):
                # START (LEFT or TOP) and SIZE (WIDTH or HEIGHT)
                pass

            elif matches == (False, True, False):
                # SIZE (WIDTH or HEIGHT)
                pass

            elif matches == (False, True, True):
                # SIZE (WIDTH or HEIGHT) and END (RIGHT or BOTTOM)
                pass

            elif matches == (False, False, True):
                # END (RIGHT or BOTTOM)
                pass

            elif matches == (True, False, True):
                # START (LEFT or TOP) and END (RIGHT or BOTTOM
                pass

            else:
                # Unhandled case
                pass
