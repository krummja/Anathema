import logging
import os.path
import sys

logger = logging.getLogger(__file__)


# This is the root Anathema directory
ROOTDIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
logger.debug("rootdir: %s", ROOTDIR)

# This is the root src directory containing start.py
BASEDIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
logger.debug("basedir: %s", BASEDIR)

# This is the lib directory containing local versions of external libs
LIBDIR = os.path.join(BASEDIR, "lib")

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
USER_CONFIG_PATH = os.path.join(USER_STORAGE_DIR, CONFIG_FILE)
logger.debug("user config: %s", USER_CONFIG_PATH)

USER_GAME_DATA_DIR = os.path.join(USER_STORAGE_DIR, "data")
logger.debug("user data: %s", USER_GAME_DATA_DIR)

USER_GAME_SAVE_DIR = os.path.join(USER_GAME_DATA_DIR, "saves")
logger.debug("save games: %s", USER_GAME_SAVE_DIR)
