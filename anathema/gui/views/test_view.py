from __future__ import annotations
from typing import *

from anathema.gui.view import View

from anathema.console import console
from anathema.lib.morphism import *

if TYPE_CHECKING:
    from gui.screen import Screen
    from tcod.event import KeyboardEvent


class TestView(View):
    
    def __init__(self) -> None:
        super().__init__()
        
    def perform_draw(self) -> None:
        console.draw_frame(Rect(Point(0, 0), Size(20, 3)), fg=(255, 255, 255), bg=(21, 21, 21))

    def handle_input(self, event: KeyboardEvent) -> bool:
        return True


class TestView2(View):
    
    def __init__(self) -> None:
        super().__init__()
        self._bounds = Rect(Point(21, 0), Size(20, 20))

    def perform_draw(self) -> None:
        console.draw_frame(self.bounds, title="Test Panel", fg=(255, 255, 255), bg=(21, 21, 21))
        
    def handle_input(self, event: KeyboardEvent) -> bool:
        return True
