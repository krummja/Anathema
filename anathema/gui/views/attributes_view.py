from __future__ import annotations
from typing import *

from anathema.gui.view import View
from anathema.lib.morphism import *
from anathema.console import console

if TYPE_CHECKING:
    from anathema.typedefs import Color
    from anathema.gui.screen import Screen
    from anathema.lib.ecstremity import Entity


class AttributesView(View):

    def __init__(
            self,
            point: Point,
            entity: Entity
        ) -> None:
        super().__init__()
        self.point = point
        self.entity = entity
        self._bounds = Rect(self.point, Size(40, 5))

    def perform_draw(self) -> None:
        print_ = self.screen.console.print
        x: int = int(self.point.x)
        y: int = int(self.point.y)
        fg = (255, 255, 255)
        bg = (21, 21, 21)
        offset = 4

        print_(Point(x, y),   "MIG", fg, bg)
        print_(Point(x, y+1), "FIN", fg, bg)
        print_(Point(x, y+2), "VIT", fg, bg)
        print_(Point(x, y+3), "PIE", fg, bg)
        print_(Point(x, y+4), "CUN", fg, bg)
        print_(Point(x, y+5), "KNO", fg, bg)

        print_(Point(x + offset, y),   f"{self.entity['ATTRIBUTES']['might']}", fg, bg)
        print_(Point(x + offset, y+1), f"{self.entity['ATTRIBUTES']['finesse']}", fg, bg)
        print_(Point(x + offset, y+2), f"{self.entity['ATTRIBUTES']['vitality']}", fg, bg)
        print_(Point(x + offset, y+3), f"{self.entity['ATTRIBUTES']['piety']}", fg, bg)
        print_(Point(x + offset, y+4), f"{self.entity['ATTRIBUTES']['cunning']}", fg, bg)
        print_(Point(x + offset, y+5), f"{self.entity['ATTRIBUTES']['knowledge']}", fg, bg)
