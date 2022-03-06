from __future__ import annotations
from typing import *

from gui.screen import Screen
from anathema.gui.views import *
from anathema.lib.morphism import *

if TYPE_CHECKING:
    from anathema.client import Client


class TestScreen(Screen):
    
    def __init__(self, client: Client) -> None:
        super().__init__(client)

        # test_view = TestView2()
        # self.add_view(test_view)
        # Snap(test_view).left().center()
        #
        # self.add_view(TextField(
        #     point = Point(42, 30),
        #     text = "Testing the TextField view!",
        #     fg = (255, 0, 255)
        # ))
        # self.add_view(Button(
        #     point = Point(42, 35),
        #     text = "Test Button",
        # ))
        # self.add_view(Button(
        #     point = Point(42, 38),
        #     text = "Test Button",
        #     callback = self.client.quit
        # ))
        #
        # group_1 = HorizontalGroup(
        #     self,
        #     Point(5, 0),
        #     [
        #         TextField(Point(0, 0), "Test string"),
        #         TextField(Point(0, 0), "Test string"),
        #         TextField(Point(0, 0), "Test string"),
        #         TextField(Point(0, 0), "Test string"),
        #         TextField(Point(0, 0), "Test string"),
        #     ],
        #     padding = 1,
        #     spacing = 3
        # )
        # self.add_view(group_1)

        # button_group = VerticalGroup(
        #     self,
        #     Point(0, 0),
        #     [
        #         Button("Test", Point(0, 0)),
        #         Button("Test", Point(0, 0)),
        #         Button("Test", Point(0, 0)),
        #     ],
        #     padding = 1,
        #     spacing = 1
        # )
        # self.add_view(button_group)
        # Snap(button_group).bottom().left()

    def cmd_quit(self) -> None:
        self.client.quit()
