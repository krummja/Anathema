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


class LayoutType(Enum):
    FRAME = 1
    INTRINSIC = 2


class _Type(Enum):
    NONE = 0
    FRAME = 1
    INTRINSIC = 2
    CONSTANT = 3
    FRACTION = 4
    UNKNOWN = 5


class Layout:

    def __init__(
            self, /,
            top: Optional[Number | LayoutType] = 0,
            right: Optional[Number | LayoutType] = 0,
            bottom: Optional[Number | LayoutType] = 0,
            left: Optional[Number | LayoutType] = 0,
            width: Optional[Number | LayoutType] = None,
            height: Optional[Number | LayoutType] = None,
    ) -> None:
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left
        self.width = width
        self.height = height

    def get_value(self, key: str, view: View) -> Number | Size | None:
        """ Get the value of the provided attribute key on this Layout.
        Key will be one of {'top', 'right', 'bottom', 'left', 'width', 'height'}
        """

        # Map the key to its local attribute, then return the internal type (_Type):
        _type = self._get_attribute_type(key)

        # Then check each type case:
        if _type == _Type.NONE:
            raise ValueError("This value is not applicable to the current View.")
        elif _type == _Type.FRAME:
            frame: Rect = view.bounds
            assert view.parent is not None
            return {
                'top': frame.y,
                'bottom': view.parent.bounds.height - frame.bottom,
                'left': frame.x,
                'right': view.parent.bounds.width - frame.right,
                'width': frame.width,
                'height': frame.height
            }.get(key)

        elif _type == _Type.INTRINSIC:
            pass
        elif _type == _Type.CONSTANT:
            return getattr(self, key)
        elif _type == _Type.FRACTION:
            assert view.parent is not None
            value = getattr(self, key)
            if key in ('left', 'width', 'right'):
                return view.parent.bounds.width * value
            elif key in ('top', 'height', 'bottom'):
                return view.parent.bounds.height * value
            else:
                raise KeyError("Unknown key:", key)
        return None

    def _get_attribute_type(self, key: str) -> _Type:
        """ Map an attribute key to an internal type (_Type).

        Valid keys can be from:
            {'top', 'bottom', 'left', 'right', 'width', 'height'}

        If the attribute exists on the Layout, check its value against expected
        internal _Type enum.

        Attribute values can be from:
            {None, LayoutType, int, float}

        Return an appropriate _Type based on the attribute value, or throw
        a ValueError if the attribute is an unhandled type.
        """
        attribute: None | LayoutType | Number = getattr(self, key)

        if attribute is None:
            return _Type.NONE
        elif attribute == LayoutType.FRAME:
            return _Type.FRAME
        elif attribute == LayoutType.INTRINSIC:
            return _Type.INTRINSIC
        elif isinstance(attribute, int) or isinstance(attribute, float):
            if attribute >= 1:
                return _Type.CONSTANT
            return _Type.FRACTION
        raise ValueError(f"Unknown type for option {key}: {type(key)}")


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
                raise ValueError("Invalid layout definition. Aborting.")

            elif matches == (True, False, False):
                # START (LEFT or TOP)
                coord_value = layout.get_value(field_start, self.view)
                size_value = getattr(layout, field_size)
                setattr(final_frame, field_coord, coord_value)
                setattr(final_frame, field_size, size_value)

            elif matches == (True, True, False):
                # START (LEFT or TOP) and SIZE (WIDTH or HEIGHT)
                start_value = layout.get_value(field_start, self.view)
                size_value = layout.get_value(field_size, self.view)
                setattr(final_frame, field_start, start_value)
                setattr(final_frame, field_size, size_value)

            elif matches == (False, True, False):
                # SIZE (WIDTH or HEIGHT)
                size_value = layout.get_value(field_size, self.view)
                coord_value = getattr(parent_bounds, field_size) / 2 - size_value / 2
                setattr(final_frame, field_size, size_value)
                setattr(final_frame, field_coord, coord_value)

            elif matches == (False, True, True):
                # SIZE (WIDTH or HEIGHT) and END (RIGHT or BOTTOM)
                size_value = layout.get_value(field_size, self.view)
                coord_value = getattr(parent_bounds, field_size) - layout.get_value(field_end, self.view) - size_value
                setattr(final_frame, field_size, size_value)
                setattr(final_frame, field_coord, coord_value)

            elif matches == (False, False, True):
                # END (RIGHT or BOTTOM)
                size_value = getattr(layout, field_size)
                coord_value = getattr(parent_bounds, field_size) - layout.get_value(field_end, self.view)
                setattr(final_frame, field_size, size_value)
                setattr(final_frame, field_coord, coord_value)

            elif matches == (True, False, True):
                # START (LEFT or TOP) and END (RIGHT or BOTTOM)
                start_value = layout.get_value(field_start, self.view)
                end_value = getattr(parent_bounds, field_size) - start_value - layout.get_value(field_end, self.view)
                setattr(final_frame, field_coord, start_value)
                setattr(final_frame, field_size, end_value)

            else:
                raise ValueError("Unhandled case. Aborting.")

        assert (final_frame.x != -1000)
        assert (final_frame.y != -1000)
        assert (final_frame.width != -1000)
        assert (final_frame.height != -1000)
        self.view.bounds = final_frame.floored
