from __future__ import annotations
from typing import TYPE_CHECKING

from morphism import (Point, Rect, Size)  # type: ignore


if TYPE_CHECKING:
    from anathema.typedefs import *
    from view import View
    from anathema.typedefs import Number


class Layout:
    """Base layout object.

    The :py:class:`Layout` class defines the layout model properties for all
    UI elements. It is based on a springs-and-struts model, where
    :py:class:`View` instances act as containers for subviews. Each view
    manages the layout of its child elements.

    Values passed into the constructor can conflict with one another. In such
    cases, the layout's behavior is undefined.
    """

    def __init__(
            self,
            width: Optional[Number] = None,
            height: Optional[Number] = None,
            top: Optional[Number] = 0,
            right: Optional[Number] = 0,
            bottom: Optional[Number] = 0,
            left: Optional[Number] = 0,
        ) -> None:
        """
        Constructor.

        .. py:attribute:: width
        Constrain the view width.

        .. py:attribute:: height
        Constrain the view height.

        .. py:attribute:: top
        Constrain the view's distance from the top edge of its superview.

        .. py:attribute:: right
        Constrain the view's distance from the right edge of its superview.

        .. py:attribute:: bottom
        Constrain the view's distance from the bottom edge of its superview.

        .. py:attribute:: left
        Constrain the view's distance from the left edge of its superview.
        """
        self.width = width
        self.height = height
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

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
        """
        Create a :py:class:`Layout` object that positions the view in the
        center of the superview with a constant width and height.
        """
        return Layout(
            top=None, bottom=None, left=None, right=None,
            width=width, height=height)

    @classmethod
    def column_left(cls, width: Number) -> Layout:
        """
        Create a :py:class:`Layout` object that positions the view as a
        full-height left column with a constant width.
        """
        return Layout(
            top=0, bottom=0, left=0, right=None,
            width=width, height=None)

    @classmethod
    def column_right(cls, width: Number) -> Layout:
        """
        Create a :py:class:`Layout` object that positions the view as a
        full-height right column with a constant width.
        """
        return Layout(
            top=0, bottom=0, left=None, right=0,
            width=width, height=None)

    @classmethod
    def row_top(cls, height: Number) -> Layout:
        """
        Create a :py:class:`Layout` object that positions the view as a
        full-height top row with a constant height.
        """
        return Layout(
            top=0, bottom=None, left=0, right=0,
            width=None, height=height)

    @classmethod
    def row_bottom(cls, height: Number) -> Layout:
        """
        Create a :py:class:`Layout` object that positions the view as a
        full-height bottom row with a constant height.
        """
        return Layout(
            top=None, bottom=0, left=0, right=0,
            width=None, height=height)

    # Convenience modifiers ###

    def with_updates(self, kwargs: Mapping[str, Optional[float]]) -> Layout:
        """
        Returns a new :py:class:`Layout` object with the given changes to its
        attributes. For example, here's a view with a constant width, on the
        right side of its superview, with half the height of its superview:

           # "right column, but only half height"
           Layout.column_right(10).with_updates(bottom=0.5)
        """
        opts = self.opts
        opts.update(kwargs)
        return Layout(**opts)

    # Semi-internal layout API ###

    def get_type(self, k: str) -> str:
        """Return one of ``{'none', 'frame', 'constant', 'fraction'}``."""
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
