from __future__ import annotations
from typing import *
from anathema.lib.morphism import (Rect, Point, Size)

from anathema.gui.layout import Layout
from anathema.console import console

if TYPE_CHECKING:
    from tcod.event import KeyboardEvent, TextInput
    from anathema.screen import Screen
    from anathema.typedefs import Number


ZERO_RECT = Rect(Point(0, 0), Size(0, 0))


class UIHierarchyBase:

    def __init__(
            self,
            layout: Optional[Layout] = None,
            frame: Optional[Rect] = None
        ) -> None:
        self.needs_layout: bool = True
        self.subviews: List[UIHierarchyBase] = []
        self.superview: Optional[UIHierarchyBase] = None

        if not frame:
            self._frame = ZERO_RECT
        else:
            self._frame = frame
        self._bounds = self._frame.with_origin(Point(0, 0))

        self.layout_spec = frame
        if not layout:
            self.layout_options = Layout()
        else:
            self.layout_options = layout

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
        self.needs_layout = True

    @property
    def frame(self) -> Rect:
        return self._frame

    @frame.setter
    def frame(self, value: Rect) -> None:
        if value == self._frame:
            return
        self._frame = value
        self._bounds = value.with_origin(Point(0, 0))
        self.needs_layout = True

    @property
    def ancestors(self) -> Generator[UIHierarchyBase, Any, None]:
        view: UIHierarchyBase = self.superview
        while view:
            yield view
            view = view.superview

    @property
    def leftmost_leaf(self) -> UIHierarchyBase:
        if self.subviews:
            return self.subviews[0].leftmost_leaf
        else:
            return self

    @property
    def postorder_traversal(self) -> Generator[UIHierarchyBase, Any, None]:
        for v in self.subviews:
            yield from v.postorder_traversal
        yield self

    def get_ancestor_matching(
            self,
            predicate: Callable[[Optional[UIHierarchyBase]], bool]
        ) -> Optional[UIHierarchyBase]:
        view = self.superview
        for _ in self.ancestors:
            if predicate(view):
                return view
        return None

    def add_subviews(self, subviews: List[UIHierarchyBase]) -> None:
        for v in subviews:
            v.superview = self
        self.subviews.extend(subviews)

    def remove_subviews(self, subviews: List[UIHierarchyBase]) -> None:
        for v in subviews:
            v.superview = None
        self.subviews = [v for v in self.subviews if v not in subviews]

    def add_subview(self, subview: UIHierarchyBase) -> None:
        self.add_subviews([subview])

    def remove_subview(self, subview: UIHierarchyBase) -> None:
        self.remove_subviews([subview])

    def perform_layout(self) -> None:
        if self.needs_layout:
            self.layout_subviews()
            self.needs_layout = False
        for view in self.subviews:
            view.perform_layout()

    def layout_subviews(self) -> None:
        for view in self.subviews:
            view.apply_springs_and_struts_layout()

    def apply_springs_and_struts_layout(self):
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
                    options.get_value(field_start, case(View, self)))
                # pretend that size is constant from frame
                setattr(
                    final_frame, field_size,
                    getattr(spec, field_size))

            elif matches == (True, True, False):
                # start, size           defined
                # end                   undefined
                setattr(
                    final_frame, field_coord,
                    options.get_value(field_start, cast(View, self)))
                setattr(
                    final_frame, field_size,
                    options.get_value(field_size, cast(View, self)))

            elif matches == (False, True, False):  # magical centering!
                # start, end            undefined
                # size                  defined
                size_val: Union[Number, Size] = options.get_value(field_size, cast(View, self))
                setattr(final_frame, field_size, size_val)
                setattr(
                    final_frame, field_coord,
                    getattr(superview_bounds, field_size) / 2 - size_val / 2)

            elif matches == (False, True, True):
                size_val = options.get_value(field_size, cast(View, self))
                setattr(
                    final_frame, field_coord,
                    getattr(superview_bounds, field_size) - options.get_value(field_end, cast(View, self)) - size_val)
                setattr(final_frame, field_size, size_val)

            elif matches == (False, False, True):
                setattr(
                    final_frame, field_coord,
                    getattr(superview_bounds, field_size) - options.get_value(field_end, cast(View, self)))
                # pretend that size is constant from frame
                setattr(final_frame, field_size, getattr(spec, field_size))

            elif matches == (True, False, True):
                start_val = options.get_value(field_start, cast(View, self))
                end_val = options.get_value(field_end, cast(View, self))
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


class UIResponderBase(UIHierarchyBase):

    def __init__(
            self,
            layout: Optional[Layout] = None,
            frame: Optional[Rect] = None
        ) -> None:
        super().__init__(layout, frame)
        self.first_responder: Optional[UIResponderBase] = None
        self.is_first_responder: bool = False
        self.is_hidden: bool = False

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
    def first_responder_container_view(self) -> Optional[UIResponderBase]:
        if self.first_responder:
            return self
        for view in self.ancestors:
            if view.first_responder:
                return view
        return None

    def descendant_did_become_first_responder(self, view: UIResponderBase) -> bool:
        pass

    def descendant_did_resign_first_responder(self, view: UIResponderBase) -> bool:
        pass


class View(UIResponderBase):

    def __init__(
            self,
            layout: Optional[Layout] = None,
            frame: Optional[Rect] = None
        ) -> None:
        super(View, self).__init__(layout, frame)

    def handle_input(self, event: KeyboardEvent) -> bool:
        pass

    def handle_textinput(self, event: TextInput) -> bool:
        pass

    def draw(self) -> None:
        pass

    def perform_draw(self) -> None:
        if self.is_hidden:
            return
        self.draw()
        assert console is not None
        for view in self.subviews:
            with console.translate(view.frame.origin):
                view.perform_draw()


if __name__ == '__main__':
    view1 = View(frame = Rect(Point(0, 0), Size(0, 0)))
