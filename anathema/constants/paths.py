import logging
import os.path
import sys

logger = logging.getLogger(__file__)


# This is the root Anathema directory
LIBDIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
logger.debug("libdir: %s", LIBDIR)

# This is the root src directory containing start.py
BASEDIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
logger.debug("basedir: %s", BASEDIR)

# Static assets like font files
ASSETDIR = os.path.join(BASEDIR, "assets")

# ECStremity-related files like Prefabs
DATADIR = os.path.join(BASEDIR, "data")
COMPONENTS = os.path.join(DATADIR, "components")
PREFABS = os.path.join(DATADIR, "prefabs/")

# Defaults to "~/.anathema.d/"
USER_STORAGE_DIR = os.path.join(os.path.expanduser("~"), ".anathema.d")
logger.debug("userdir: %s", USER_STORAGE_DIR)

CONFIG_FILE = "anathema.cfg"
# "~/.anathema.d/anathema.cfg"
USER_CONFIG_PATH = os.path.join(USER_STORAGE_DIR, CONFIG_FILE)
logger.debug("user config: %s", USER_CONFIG_PATH)

# "~/.anathema.d/data/"
USER_GAME_DATA_DIR = os.path.join(USER_STORAGE_DIR, "data")
logger.debug("user data: %s", USER_GAME_DATA_DIR)

# "~/.anathema.d/data/saves/"
USER_GAME_SAVE_DIR = os.path.join(USER_GAME_DATA_DIR, "saves")
logger.debug("save games: %s", USER_GAME_SAVE_DIR)
