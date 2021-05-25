from __future__ import annotations
from typing import TYPE_CHECKING, List

from morphism import (Rect)  # type: ignore

from anathema.screen import Screen

if TYPE_CHECKING:
    from anathema.client import Client
    from anathema.views.view import View


class MainMenu(Screen):

    def __init__(self, client: Client) -> None:
        self.views: List[View] = []
        super().__init__(client=client, views=self.views)

