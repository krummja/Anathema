from __future__ import annotations
from typing import *

from anathema.console import console
import anathema.prepare as prepare
from anathema.lib.morphism import *

if TYPE_CHECKING:
    from anathema.gui.view import View


class Snap:

    @staticmethod
    def to_bottom(view: View) -> None:
        screen_bounds = view.screen.bounds
        view_bounds = view.bounds
        point = Point(
            view_bounds.x,
            screen_bounds.height - view_bounds.height
        )
        view.bounds = Rect(point, view_bounds.size)

    @staticmethod
    def to_left(view: View) -> None:
        point = Point(0, view.bounds.y)
        view.bounds = Rect(point, view.bounds.size)

    @staticmethod
    def to_bottom_left(view: View) -> None:
        Snap.to_bottom(view)
        Snap.to_left(view)
