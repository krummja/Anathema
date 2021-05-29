from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional, Iterator, cast
from morphism import (Rect, Point, Size)  # type: ignore
import tcod

from view import View
from anathema.views.layout import Layout

if TYPE_CHECKING:
    from tcod.event import KeyboardEvent, TextInput
    from anathema.screen import Screen


class FirstResponderContainerView(View):
    """
    Root container view for all subview types.
    """

    def __init__(
            self,
            screen: Optional[Screen] = None,
            layout: Optional[Layout] = None,
            subviews: Optional[List[View]] = None,
            frame: Optional[Rect] = None
        ) -> None:
        super().__init__(screen, layout, subviews, frame)
        self.first_responder: Optional[View] = None
        self.find_next_responder()

    @property
    def intrinsic_size(self) -> Optional[Size]:
        return None

    @property
    def contains_first_responders(self) -> bool:
        return True

    def first_responder_traversal(self) -> Iterator[View]:
        for subview in self.subviews:
            yield from self._first_responder_traversal(subview)

    def _first_responder_traversal(self, view: View) -> Iterator[View]:
        if view.contains_first_responders:
            yield view
            return
        for subview in view.subviews:
            yield from self._first_responder_traversal(subview)
        yield view

    @property
    def _eligible_first_responders(self) -> List[View]:
        return [v for v in self.first_responder_traversal()
                if v != self and v.can_become_first_responder]

    def remove_subviews(self, subviews: List[View]) -> None:
        super().remove_subviews(subviews)
        for view in subviews:
            for subview in self._first_responder_traversal(view):
                if subview == self.first_responder:
                    self.set_first_responder(None)
                    self.find_next_responder()
                    return

    def set_first_responder(self, value: Optional[View]) -> None:
        if self.first_responder:
            self.first_responder.did_resign_first_responder()
            for ancestor in self.first_responder.ancestors:
                ancestor.descendant_did_resign_first_responder(self.first_responder)

        self.first_responder = value

        if self.first_responder:
            self.first_responder.did_become_first_responder()
            for ancestor in self.first_responder.ancestors:
                ancestor.descendant_did_become_first_responder(self.first_responder)

    def find_next_responder(self) -> None:
        existing_responder = self.first_responder
        if self.first_responder is None:
            existing_responder = self.leftmost_leaf
        all_responders = self._eligible_first_responders

        try:
            i = all_responders.index(cast(View, existing_responder))
            if i == len(all_responders) - 1:
                self.set_first_responder(all_responders[0])
            else:
                self.set_first_responder(all_responders[i+1])

        except ValueError:
            if all_responders:
                self.set_first_responder(all_responders[0])
            else:
                self.set_first_responder(None)

    def find_prev_responder(self) -> None:
        existing_responder = self.first_responder
        if self.first_responder is None:
            existing_responder = self.leftmost_leaf
        all_responders = self._eligible_first_responders

        try:
            i = all_responders.index(cast(View, existing_responder))
            if i == 0:
                self.set_first_responder(all_responders[-1])
            else:
                self.set_first_responder(all_responders[i-1])

        except ValueError:
            if all_responders:
                self.set_first_responder(all_responders[-1])
            else:
                self.set_first_responder(None)

    def handle_textinput(self, event: TextInput) -> bool:
        handled = self.first_responder and self.first_responder.handle_textinput(event)
        if self.first_responder and not handled:
            for view in self.first_responder.ancestors:
                if view == self:
                    break
                if view.handle_textinput(event):
                    return True
        return False

    def handle_input(self, event: KeyboardEvent) -> bool:
        handled = self.first_responder and self.first_responder.handle_input(event)
        if self.first_responder and not handled:
            for v in self.first_responder.ancestors:
                if v == self:
                    break
                if v.handle_input(event):
                    return True

        can_resign = (not self.first_responder or self.first_responder.can_resign_first_responder)
        return self.handle_input_after_first_responder(event, can_resign)

    def handle_input_after_first_responder(self, event: KeyboardEvent, can_resign: bool) -> bool:
        if can_resign and event.sym == tcod.event.K_TAB:
            if event.mod & tcod.event.KMOD_LSHIFT:
                self.find_prev_responder()
                return True
            else:
                self.find_next_responder()
                return True
        return False
