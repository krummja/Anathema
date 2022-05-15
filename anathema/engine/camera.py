from __future__ import annotations
from typing import *
import numpy as np

from anathema.lib.morphism import *
from anathema import prepare
from anathema.console import console

if TYPE_CHECKING:
    from anathema.engine.engine import EngineLoop


class Camera:

    def __init__(self, loop: EngineLoop):
        self.loop = loop
        self._camera_pos: Tuple[int, int] = (0, 0)
        self.centered: bool = False
        if self.centered:
            self._view_rect: Rect = Rect(Point(0, 0), Size(*prepare.CONSOLE_SIZE))
        else:
            self._view_rect: Rect = Rect(Point(0, 0), Size(prepare.STAGE_PANEL_WIDTH, prepare.STAGE_PANEL_HEIGHT))

    @property
    def view_rect(self) -> Rect:
        return self._view_rect

    @view_rect.setter
    def view_rect(self, value: Rect) -> None:
        self._view_rect = value

    @property
    def camera_pos(self) -> Tuple[int, int]:
        if self.centered:
            cam_x = self._camera_pos[0] - prepare.CONSOLE_SIZE[0] // 2
            cam_y = self._camera_pos[1] - prepare.CONSOLE_SIZE[1] // 2
        else:
            cam_x = self._camera_pos[0] - prepare.STAGE_PANEL_WIDTH // 2
            cam_y = self._camera_pos[1] - prepare.STAGE_PANEL_HEIGHT // 2
        return cam_x, cam_y

    @camera_pos.setter
    def camera_pos(self, value):
        self._camera_pos = value

    def camera_view(
            self,
            width: int,
            height: int,
            max_width: int = prepare.STAGE_PANEL_WIDTH,
            max_height: int = prepare.STAGE_PANEL_HEIGHT
        ) -> Tuple[Tuple[slice, slice], Tuple[slice, slice]]:
        cam_x, cam_y = self.camera_pos

        screen_left = max(0, -cam_x)
        screen_top  = max(0, -cam_y)
        world_left  = max(0,  cam_x)
        world_top   = max(0,  cam_y)

        screen_width  = min(max_width  - screen_left, width  - world_left)
        screen_height = min(max_height - screen_top,  height - world_top )

        screen_view = np.s_[
                      screen_top  : screen_top  + screen_height,
                      screen_left : screen_left + screen_width
                      ]
        world_view = np.s_[
                     world_top  : world_top  + screen_height,
                     world_left : world_left + screen_width
                     ]

        return screen_view, world_view

    def camera_debug(self):
        console.draw_frame(
            Rect(
                Point(0, 0),
                Size(prepare.STAGE_PANEL_WIDTH, prepare.STAGE_PANEL_HEIGHT)),
            clear = False
        )
