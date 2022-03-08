"""This module initializes the display and creates dictionaries of resources.
It contains all the static and dynamic variables used throughout the game, such
as display resolution, scale, etc.
"""

from __future__ import annotations

import os.path
from typing import TYPE_CHECKING

import tcod.console

import anathema.config as config
import anathema.constants.paths as paths

if TYPE_CHECKING:
    pass


if not os.path.isdir(paths.USER_STORAGE_DIR):
    os.makedirs(paths.USER_STORAGE_DIR)

# Create game dir if missing
if not os.path.isdir(paths.USER_GAME_DATA_DIR):
    os.makedirs(paths.USER_GAME_DATA_DIR)

# Create game data dir if missing
if not os.path.isdir(paths.USER_GAME_SAVE_DIR):
    os.makedirs(paths.USER_GAME_SAVE_DIR)

# Create game save dir if missing
config.generate_default_config()


def fetch_asset(path: str) -> str:
    return os.path.join(paths.ASSETDIR, path)


CONFIG = config.AnathemaConfig(paths.USER_CONFIG_PATH)
with open(paths.USER_CONFIG_PATH, "w") as fp:
    CONFIG.cfg.write(fp)


COLUMNS = 10
ROWS = 8

TILE_SIZE = 16
CONSOLE_SIZE = (100, 60)
STAGE_PANEL_WIDTH = 76
STAGE_PANEL_HEIGHT = 48
TILESET = tcod.tileset.load_tilesheet(fetch_asset(CONFIG.tileset), 32, 8, tcod.tileset.CHARMAP_CP437)
VSYNC = CONFIG.vsync

SAVE_PATH = os.path.join(paths.USER_GAME_SAVE_DIR, "slot")
SAVE_METHOD = ("JSON", "CBOR")[0]
