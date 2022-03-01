from __future__ import annotations
from typing import TYPE_CHECKING, Any, List, Dict, Optional, cast, Generator, Callable, Union, no_type_check
from morphism import (Rect, Point, Size)  # type: ignore

from anathema.views.layout import Layout
from anathema.console import console

if TYPE_CHECKING:
    from tcod.event import KeyboardEvent, TextInput
    from anathema.screen import Screen
    from anathema.typedefs import Number


ZERO_RECT = Rect(Point(0, 0), Size(0, 0))


def add_subviews(view: View, subviews: List[View]) -> None:
    for v in subviews:
        v.superview = view
    view.subviews.extend(subviews)


def remove_subviews(view: View, subviews: List[View]) -> None:
    for v in subviews:
        v.superview = None
    view.subviews = [v for v in view.subviews if v not in subviews]


def add_subview(view: View, subview: View) -> None:
    add_subviews(view, [subview])


def remove_subview(view: View, subview: View) -> None:
    remove_subviews(view, [subview])


class ViewItem:

    def __init__(self) -> None:
        self.superview: ViewItem | None = None


class View:

    def __init__(
            self: View,
            screen: Optional[Screen] = None,
            layout: Optional[Layout] = None,
            subviews: Optional[List[View]] = None,
            frame: Optional[Rect] = None
        ) -> None:
        if not frame:
            self._frame = ZERO_RECT
        else:
            self._frame = frame

        self._screen = screen
        self._superview: Optional[View] = None
        self._bounds = self._frame.with_origin(Point(0, 0))
        self.needs_layout: bool = True

        self.first_responder: Optional[View] = None
        self.is_first_responder: bool = False
        self.is_hidden: bool = False

        self.subviews: List[View] = []
        add_subviews(self, subviews if subviews else [])
        self.layout_spec = frame

        if not layout:
            self.layout_options = Layout()
        else:
            self.layout_options = layout

    @property
    def screen(self) -> Screen:
        if self._screen:
            return self._screen
        else:
            assert self._superview is not None
            return self._superview.screen

    @property
    def superview(self) -> Optional[View]:
        try:
            return self._superview
        except AttributeError:
            return None

    @superview.setter
    def superview(self, value: View) -> None:
        self._superview = value

    def set_needs_layout(self, value: bool = True) -> None:
        self.needs_layout = value

    def perform_draw(self) -> None:
        if self.is_hidden:
            return
        self.draw()
        assert console is not None
        for view in self.subviews:
            with console.translate(view.frame.origin):
                view.perform_draw()

    def draw(self) -> None:
        pass

    def perform_layout(self) -> None:
        if self.needs_layout:
            self.layout_subviews()
            self.needs_layout = False
        for view in self.subviews:
            view.perform_layout()

    def layout_subviews(self) -> None:
        for view in self.subviews:
            view.apply_springs_and_struts_layout_in_superview()

    @property
    def intrinsic_size(self) -> Optional[Size]:
        return None

    @property
    def frame(self) -> Rect:
        return self._frame

    @frame.setter
    def frame(self, value: Rect) -> None:
        if value == self._frame:
            return
        self._frame = value
        self._bounds = value.with_origin(Point(0, 0))
        self.set_needs_layout(True)

    @property
    def bounds(self) -> Rect:
        return self._bounds

    @bounds.setter
    def bounds(self, value: Rect) -> None:
        if value.origin != Point(0, 0):
            raise ValueError("Bounds is always anchored at (0, 0)")
        if value == self._bounds:
            return
        self._bounds = value
        self._frame = self._frame.with_size(value.size)
        self.set_needs_layout(True)

    @property
    def can_become_first_responder(self) -> bool:
        return False

    @property
    def contains_first_responders(self) -> bool:
        return False

    @property
    def can_resign_first_responder(self) -> bool:
        return True

    @property
    def first_responder_container_view(self) -> Optional[View]:
        if self.first_responder:
            return self
        for view in self.ancestors:
            if view.first_responder:
                return view
        return None

    def did_become_first_responder(self) -> None:
        self.set_needs_layout(True)
        self.is_first_responder = True

    def did_resign_first_responder(self) -> None:
        self.set_needs_layout(True)
        self.is_first_responder = False

    def descendant_did_become_first_responder(self, view: View) -> bool:
        pass

    def descendant_did_resign_first_responder(self, view: View) -> bool:
        pass

    # noinspection PyMethodMayBeStatic
    def handle_input(self, event: KeyboardEvent) -> bool:
        return False

    # noinspection PyMethodMayBeStatic
    def handle_textinput(self, event: TextInput) -> bool:
        return False

    @property
    def leftmost_leaf(self) -> View:
        if self.subviews:
            return self.subviews[0].leftmost_leaf
        else:
            return self

    @property
    def postorder_traversal(self) -> Generator[View, Any, None]:
        for v in self.subviews:
            yield from v.postorder_traversal
        yield self

    @property
    def ancestors(self) -> Generator[View, Any, None]:
        view = self.superview
        while view:
            yield view
            view = view.superview

    def get_ancestor_matching(self, predicate: Callable[[Optional[View]], bool]) -> Optional[View]:
        view = self.superview
        for _ in self.ancestors:
            if predicate(view):
                return view
        return None

    def apply_springs_and_struts_layout_in_superview(self) -> None:

        options = self.layout_options
        spec = self.layout_spec

        assert self.superview is not None
        superview_bounds = self.superview.bounds

        fields = [('left', 'right', 'x', 'width'),
                  ('top', 'bottom', 'y', 'height')]

        final_frame = Rect(Point(-1000, -1000), Size(-1000, -1000))

        for field_start, field_end, field_coord, field_size in fields:

            debug_string = options.get_debug_string_for_keys(
                [field_start, field_size, field_end])

            matches = (options.get_is_defined(field_start),
                       options.get_is_defined(field_size),
                       options.get_is_defined(field_end))

            if matches == (True, True, True):
                # start, size, end      defined
                raise ValueError(
                    "Invalid spring/strut definition: {}".format(debug_string))

            if matches == (False, False, False):
                # start, size, end      undefined
                raise ValueError(
                    "Invalid spring/strut definition: {}".format(debug_string))

            elif matches == (True, False, False):
                # start                 defined
                # size, end             undefined
                setattr(
                    final_frame, field_coord,
                    options.get_value(field_start, self))
                # pretend that size is constant from frame
                setattr(
                    final_frame, field_size,
                    getattr(spec, field_size))

            elif matches == (True, True, False):
                # start, size           defined
                # end                   undefined
                setattr(
                    final_frame, field_coord,
                    options.get_value(field_start, self))
                setattr(
                    final_frame, field_size,
                    options.get_value(field_size, self))

            elif matches == (False, True, False):  # magical centering!
                # start, end            undefined
                # size                  defined
                size_val: Union[Number, Size] = options.get_value(field_size, self)
                setattr(final_frame, field_size, size_val)
                setattr(
                    final_frame, field_coord,
                    getattr(superview_bounds, field_size) / 2 - size_val / 2)

            elif matches == (False, True, True):
                size_val = options.get_value(field_size, self)
                setattr(
                    final_frame, field_coord,
                    getattr(superview_bounds, field_size) - options.get_value(field_end, self) - size_val)
                setattr(final_frame, field_size, size_val)

            elif matches == (False, False, True):
                setattr(
                    final_frame, field_coord,
                    getattr(superview_bounds, field_size) - options.get_value(field_end, self))
                # pretend that size is constant from frame
                setattr(final_frame, field_size, getattr(spec, field_size))

            elif matches == (True, False, True):
                start_val = options.get_value(field_start, self)
                end_val = options.get_value(field_end, self)
                setattr(final_frame, field_coord, start_val)
                setattr(final_frame, field_size,
                        getattr(superview_bounds, field_size) - start_val - end_val)

            else:
                raise ValueError("Unhandled case: {}".format(debug_string))

        assert (final_frame.x != -1000)
        assert (final_frame.y != -1000)
        assert (final_frame.width != -1000)
        assert (final_frame.height != -1000)
        self._frame = final_frame.floored
