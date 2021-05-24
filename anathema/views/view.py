from __future__ import annotations
from typing import TYPE_CHECKING, Any, List, Dict, Optional
from morphism import (Rect, Point, Size)  # type: ignore

from anathema.views.layout import Layout

if TYPE_CHECKING:
    from tcod.event import KeyboardEvent
    from anathema.state import State


ZERO_RECT = Rect(Point(0, 0), Size(0, 0))


class View:

    def __init__(
            self,
            state: Optional[State] = None,
            layout: Optional[Layout] = None,
            subviews: Optional[List[View]] = None,
            frame: Optional[Rect] = None
        ) -> None:
        if not frame:
            self.frame = ZERO_RECT
        else:
            self.frame = frame

        self.state = state
        self._superview: Optional[View] = None

        self.layout = layout or Layout()
        self.subviews = subviews or []

    @property
    def superview(self) -> Optional[View]:
        return self._superview

    def handle_input(self, event: KeyboardEvent) -> None:
        pass

    def perform_layout(self) -> None:
        pass

    def perform_draw(self) -> None:
        pass
