from __future__ import annotations
from typing import *

import prepare
from anathema.console import console
from gui.screen import Screen
from anathema.gui.views import *
from anathema.gui.views.alignment import Snap
from anathema.lib.morphism import *
from anathema.prepare import CONSOLE_SIZE, STAGE_PANEL_WIDTH, STAGE_PANEL_HEIGHT
from anathema.gui.ui_colors import UIColors

if TYPE_CHECKING:
    from anathema.lib.ecstremity import Entity
    from anathema.client import Client


class Stage(Screen):

    player: Entity
    sidebar: RectView
    messages: RectView

    def __init__(self, client: Client) -> None:
        super().__init__(client)

    def on_enter(self, *args: List[Any]) -> None:
        self.player = self.client.session.world.get_entity("PLAYER")
        self.player_name = self.player["Moniker"].name

        self.client.loop.is_running = True

        self.client.loop.camera.camera_pos = self.client.loop.player.position
        self.client.loop.camera.view_rect = Rect(Point(21, 0), Size(CONSOLE_SIZE[0] - 20, CONSOLE_SIZE[1] - 16))
        self.client.loop.area_system.update()
        self.client.loop.fov_system.update_fov()
        self.client.loop.render_system.update()

        self._setup_ui()

    def on_leave(self, *args: List[Any]) -> None:
        self.client.loop.teardown()

    def pre_update(self) -> None:
        self.client.loop.update()

    def cmd_inventory(self) -> None:
        self.client.screens.push_screen(InventoryScreen(self.client))

    def cmd_equipment(self) -> None:
        self.client.screens.push_screen(EquipmentScreen(self.client))

    def cmd_character(self) -> None:
        self.client.screens.push_screen(CharacterScreen(self.client))

    def cmd_move(self, delta: Tuple[int, int]) -> None:
        self.client.loop.player.move(delta)

    def cmd_quit(self) -> None:
        self.client.screens.replace_screen("main")

    def _setup_ui(self) -> None:
        sidebar_rect: Rect = Rect(
            Point(STAGE_PANEL_WIDTH, 0),
            Size(CONSOLE_SIZE[0] - STAGE_PANEL_WIDTH, CONSOLE_SIZE[1]))

        message_rect: Rect = Rect(
            Point(0, STAGE_PANEL_HEIGHT),
            Size(STAGE_PANEL_WIDTH, CONSOLE_SIZE[1] - STAGE_PANEL_HEIGHT))

        self.sidebar = RectView(
            sidebar_rect.point,
            Size(sidebar_rect.width, CONSOLE_SIZE[1]),
            fg = (100, 100, 100),
            title = self.player_name)
        self.add_view(self.sidebar)

        self.messages = RectView(
            message_rect.point,
            message_rect.size,
            fg = (100, 100, 100),
            title = "Messages")
        self.add_view(self.messages)


class CharacterScreen(Screen):

    def __init__(self, client: Client) -> None:
        super().__init__(client)

        self.panel = RectView(size = Size(*CONSOLE_SIZE))
        self.add_view(self.panel)
        Snap(self.panel).center(offset = 10)

        tab_spacing: int = 2
        point = self.panel.bounds.point + 1

        tabs_width: int = 0
        self.character_tab = TextField(
            "Character",
            point = point,
            fg = UIColors.TEXT_SELECTED_FG)
        self.add_view(self.character_tab)
        tabs_width += self.character_tab.bounds.width + tab_spacing

        self.inventory_tab = TextField(
            "Inventory",
            point = Point(point.x + tabs_width, point.y),
            fg = UIColors.TEXT_UNSELECTED_FG)
        self.add_view(self.inventory_tab)
        tabs_width += self.inventory_tab.bounds.width + tab_spacing

        self.equipment_tab = TextField(
            "Equipment",
            point = Point(point.x + tabs_width, point.y),
            fg = UIColors.TEXT_UNSELECTED_FG)
        self.add_view(self.equipment_tab)
        tabs_width += self.equipment_tab.bounds.width + tab_spacing

    def cmd_inventory(self) -> None:
        self.client.screens.pop_screen()
        self.client.screens.push_screen(InventoryScreen(self.client))

    def cmd_equipment(self) -> None:
        self.client.screens.pop_screen()
        self.client.screens.push_screen(EquipmentScreen(self.client))

    def cmd_quit(self) -> None:
        self.client.screens.pop_screen()


class InventoryScreen(Screen):

    def __init__(self, client: Client) -> None:
        super().__init__(client)

        self.panel = RectView(size = Size(*CONSOLE_SIZE))
        self.add_view(self.panel)
        Snap(self.panel).center(offset = 10)

        tab_spacing: int = 2
        point = self.panel.bounds.point + 1

        tabs_width: int = 0
        self.character_tab = TextField(
            "Character",
            point = point,
            fg = UIColors.TEXT_UNSELECTED_FG)
        self.add_view(self.character_tab)
        tabs_width += self.character_tab.bounds.width + tab_spacing

        self.inventory_tab = TextField(
            "Inventory",
            point = Point(point.x + tabs_width, point.y),
            fg = UIColors.TEXT_SELECTED_FG)
        self.add_view(self.inventory_tab)
        tabs_width += self.inventory_tab.bounds.width + tab_spacing

        self.equipment_tab = TextField(
            "Equipment",
            point = Point(point.x + tabs_width, point.y),
            fg = UIColors.TEXT_UNSELECTED_FG)
        self.add_view(self.equipment_tab)
        tabs_width += self.equipment_tab.bounds.width + tab_spacing

    def cmd_equipment(self) -> None:
        self.client.screens.pop_screen()
        self.client.screens.push_screen(EquipmentScreen(self.client))

    def cmd_character(self) -> None:
        self.client.screens.pop_screen()
        self.client.screens.push_screen(CharacterScreen(self.client))

    def cmd_quit(self) -> None:
        self.client.screens.pop_screen()


class EquipmentScreen(Screen):

    def __init__(self, client: Client) -> None:
        super().__init__(client)

        self.panel = RectView(size = Size(*CONSOLE_SIZE))
        self.add_view(self.panel)
        Snap(self.panel).center(offset = 10)

        tab_spacing: int = 2
        point = self.panel.bounds.point + 1

        tabs_width: int = 0
        self.character_tab = TextField(
            "Character",
            point = point,
            fg = UIColors.TEXT_UNSELECTED_FG)
        self.add_view(self.character_tab)
        tabs_width += self.character_tab.bounds.width + tab_spacing

        self.inventory_tab = TextField(
            "Inventory",
            point = Point(point.x + tabs_width, point.y),
            fg = UIColors.TEXT_UNSELECTED_FG)
        self.add_view(self.inventory_tab)
        tabs_width += self.inventory_tab.bounds.width + tab_spacing

        self.equipment_tab = TextField(
            "Equipment",
            point = Point(point.x + tabs_width, point.y),
            fg = UIColors.TEXT_SELECTED_FG)
        self.add_view(self.equipment_tab)
        tabs_width += self.equipment_tab.bounds.width + tab_spacing

    def cmd_inventory(self) -> None:
        self.client.screens.pop_screen()
        self.client.screens.push_screen(InventoryScreen(self.client))

    def cmd_character(self) -> None:
        self.client.screens.pop_screen()
        self.client.screens.push_screen(CharacterScreen(self.client))

    def cmd_quit(self) -> None:
        self.client.screens.pop_screen()
