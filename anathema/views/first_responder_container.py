from __future__ import annotations
from typing import TYPE_CHECKING, Any, List, Dict, Optional
from morphism import (Rect, Point, Size)  # type: ignore

from anathema.views.view import View
from anathema.views.layout import Layout

if TYPE_CHECKING:
    from tcod.event import KeyboardEvent
    from anathema.state import State


class FirstResponderContainerView(View):

    def __init__(
            self,
            state: Optional[State] = None,
            layout: Optional[Layout] = None,
            subviews: Optional[List[View]] = None,
            frame: Optional[Rect] = None
        ) -> None:
        super().__init__(state, layout, subviews, frame)
        self.first_responder = None
        self.find_next_responder()
        self.frame = None

    def find_next_responder(self) -> None:
        pass

    def perform_layout(self) -> None:
        pass

    def perform_draw(self) -> None:
        pass
