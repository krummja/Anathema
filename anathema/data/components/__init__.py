import os
import importlib
import pprint
import logging

from anathema.log import bcolors, cprint
from .environment import load_environment_components

logger = logging.getLogger(__file__)

tree = os.listdir(os.path.dirname(os.path.abspath(__file__)))


def load_data_components():
    components = []
    for file in tree:
        if file[-3:] == ".py" and file[:2] != "__":
            file_name = file.replace(".py", "")
            module = importlib.import_module("." + file_name, "anathema.data.components")
            for key in module.__dict__.keys():
                if key.lower() == file_name:
                    components.append(module.__dict__[key])
    return components


components = load_data_components()
components += load_environment_components()
