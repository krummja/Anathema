from __future__ import annotations
from typing import Optional, List, Tuple, TYPE_CHECKING
from morphism import Point, Size, Rect  # type: ignore
from view import View

from anathema.console import console

if TYPE_CHECKING:
    from anathema.views.layout import Layout
    from anathema.screen import Screen


class LabelView(View):
    """Draws the given string inside its bounds. Supports multi-line strings."""

    def __init__(
            self,
            # LabelView parameters.
            text: str = "<unset>",
            fg: Tuple[int, int, int] = (255, 255, 255),
            bg: Tuple[int, int, int] = (21, 21, 21),
            align_horz: str = 'center',
            align_vert: str = 'center',
            size: Optional[Size] = None,
            # Superclass parameters.
            screen: Optional[Screen] = None,
            layout: Optional[Layout] = None,
            subviews: Optional[List[View]] = None,
            frame: Optional[Rect] = None
        ) -> None:
        super().__init__(screen, layout, subviews, frame)
        self.align_horz = align_horz
        self.align_vert = align_vert
        self.text = text
        self.fg = fg
        self.bg = bg
        self._explicit_size = size

    @property
    def intrinsic_size(self) -> Size:
        if self._explicit_size:
            return self._explicit_size
        height = 0
        width = 0
        for line in self.text.splitlines():
            height += 1
            width = max(width, len(line))
        return Size(width, height)

    def update(self, text: str) -> None:
        self.text = text

    def draw(self) -> None:
        x = 0
        if self.align_horz == 'center':
            x = self.bounds.width / 2 - self.intrinsic_size.width / 2
        elif self.align_horz == 'right':
            x = self.bounds.width - self.intrinsic_size.width

        y = 0
        if self.align_vert == 'center':
            y = self.bounds.height / 2 - self.intrinsic_size.height / 2
        elif self.align_vert == 'bottom':
            y = self.bounds.height - self.intrinsic_size.height

        console.set_fg(Rect(Point(x, y), self.intrinsic_size).floored, self.fg)
        console.set_bg(Rect(Point(x, y), self.intrinsic_size).floored, self.bg)
        console.print(Point(x, y).floored, self.text)
