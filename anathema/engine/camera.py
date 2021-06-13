from __future__ import annotations
from typing import *
import numpy as np

from anathema import prepare

if TYPE_CHECKING:
    from anathema.engine.engine import EngineLoop


class Camera:

    def __init__(self, loop: EngineLoop):
        self.loop = loop
        self._camera_pos: Tuple[int, int] = (0, 0)

    @property
    def camera_pos(self) -> Tuple[int, int]:
        cam_x = self._camera_pos[0] - prepare.STAGE_PANEL_WIDTH // 2
        cam_y = self._camera_pos[1] - prepare.STAGE_PANEL_HEIGHT // 2
        return cam_x, cam_y

    @camera_pos.setter
    def camera_pos(self, value):
        self._camera_pos = value

    def camera_view(self, width: int, height: int) -> Tuple[Tuple[slice, slice], Tuple[slice, slice]]:
        cam_x, cam_y = self.camera_pos

        screen_left = max(0, -cam_x)
        screen_top = max(0, -cam_y)
        world_left = max(0, cam_x)
        world_top = max(0, cam_y)

        screen_width = min(prepare.STAGE_PANEL_WIDTH - screen_left, width - world_left)
        screen_height = min(prepare.STAGE_PANEL_HEIGHT - screen_top, height - world_top)

        screen_view = np.s_[screen_top:screen_top+screen_height, screen_left:screen_left+screen_width]
        world_view = np.s_[world_top:world_top+screen_height, world_left:world_left+screen_width]

        return screen_view, world_view
