from __future__ import annotations
from typing import Tuple, List, TYPE_CHECKING, Optional

from view import View
from anathema.console import console

if TYPE_CHECKING:
    from anathema.views.layout import Layout
    from anathema.screen import Screen
    from morphism import Rect  # type: ignore


class RectView(View):

    def __init__(
            self,
            fg: Tuple[int, int, int] = (255, 255, 255),
            bg: Tuple[int, int, int] = (21, 21, 21),
            fill: bool = False,
            style: str = 'single',
            screen: Optional[Screen] = None,
            layout: Optional[Layout] = None,
            subviews: Optional[List[View]] = None,
            frame: Optional[Rect] = None
        ) -> None:
        super().__init__(screen, layout, subviews, frame)
        self.fg = fg
        self.bg = bg
        self.fill = fill
        self.style = style

    def draw(self) -> None:
        console.draw_frame(self.bounds, fg=self.fg, bg=self.bg)
