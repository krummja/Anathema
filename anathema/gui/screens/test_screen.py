from __future__ import annotations
from typing import *

from gui.screen import Screen

if TYPE_CHECKING:
    from anathema.client import Client
    from anathema.gui.view import View


class TestScreen(Screen):
    
    def __init__(self, client: Client) -> None:
        super().__init__(client)
    
    def cmd_quit(self) -> None:
        self.client.quit()

