from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List, Dict, Any, Mapping, Union, cast
from numbers import Real

from morphism import (Point, Rect, Size)  # type: ignore


if TYPE_CHECKING:
    from anathema.typedefs import *
    from anathema.screen import Screen
    from anathema.views.view import View
    from anathema.typedefs import Number


class Layout:
    """Base layout."""

    def __init__(
            self,
            width: Optional[Number] = None,
            height: Optional[Number] = None,
            left: Optional[Number] = 0,
            top: Optional[Number] = 0,
            right: Optional[Number] = 0,
            bottom: Optional[Number] = 0
        ) -> None:
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

        self.opts = {
            'width': width,
            'height': height,
            'left': left,
            'top': top,
            'right': right,
            'bottom': bottom
            }

    @classmethod
    def centered(cls, width: Number, height: Number) -> Layout:
        return Layout(
            top=None, bottom=None, left=None, right=None,
            width=width, height=height)

    @classmethod
    def column_left(cls, width: Number) -> Layout:
        return Layout(
            top=0, bottom=0, left=0, right=None,
            width=width, height=None)

    @classmethod
    def column_right(cls, width: Number) -> Layout:
        return Layout(
            top=0, bottom=0, left=None, right=0,
            width=width, height=None)

    @classmethod
    def row_top(cls, height: Number) -> Layout:
        return Layout(
            top=0, bottom=None, left=0, right=0,
            width=None, height=height)

    @classmethod
    def row_bottom(cls, height: Number) -> Layout:
        return Layout(
            top=None, bottom=0, left=0, right=0,
            width=None, height=height)

    # Convenience modifiers ###

    def with_updates(self, kwargs: Mapping[str, Optional[float]]) -> Layout:
        opts = self.opts
        opts.update(kwargs)
        return Layout(**opts)

    # Semi-internal layout API ###

    def get_type(self, k: str) -> str:
        val = getattr(self, k)
        if val is None:
            return 'none'
        elif val == 'frame':
            return 'frame'
        elif val == 'intrinsic':
            return 'intrinsic'
        elif isinstance(val, int) or isinstance(val, float):
            if val >= 1:
                return 'constant'
            else:
                return 'fraction'
        else:
            raise ValueError(
                "Unknown type for option {}: {}".format(k, type(k)))

    def get_is_defined(self, k: str) -> bool:
        return getattr(self, k) is not None

    def get_debug_string_for_keys(self, keys: List[str]) -> str:
        return ','.join(["{}={}".format(k, self.get_type(k)) for k in keys])

    def get_value(self, k: str, view: View) -> Optional[Union[Number, Size]]:

        if getattr(self, k) is None:
            raise ValueError("Superview isn't relevant to this value")

        if self.get_type(k) == 'constant':
            return getattr(self, k)

        elif self.get_type(k) == 'intrinsic':
            intrinsic_size: Size = view.intrinsic_size
            if k == 'width':
                return intrinsic_size[0]
            elif k == 'height':
                return intrinsic_size[1]
            else:
                raise KeyError(
                    "'intrinsic' can only be used with width or height.")

        elif self.get_type(k) == 'frame':
            layout_spec: Rect = view.layout_spec
            assert view.superview is not None
            if k == 'left':
                return layout_spec.x
            elif k == 'top':
                return layout_spec.y
            elif k == 'right':
                return view.superview.bounds.width - layout_spec.right
            elif k == 'bottom':
                return view.superview.bounds.height - layout_spec.bottom
            elif k == 'width':
                return layout_spec.width
            elif k == 'height':
                return layout_spec.height
            else:
                raise KeyError("Unknown key:", k)

        elif self.get_type(k) == 'fraction':
            assert view.superview is not None
            val = getattr(self, k)
            if k in ('left', 'width', 'right'):
                return view.superview.bounds.width * val
            elif k in ('top', 'height', 'bottom'):
                return view.superview.bounds.height * val
            else:
                raise KeyError("Unknown key:", k)
        else:
            return None
