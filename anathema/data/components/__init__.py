import os
import importlib
import pprint

tree = os.listdir("./anathema/data/components")
tree.remove("__init__.py")
tree.remove("__pycache__")

components = []
for file in tree:
    file_name = file.replace(".py", "")
    module = importlib.import_module("." + file_name, "anathema.data.components")
    for key in module.__dict__.keys():
        if key.lower() == file_name:
            components.append(module.__dict__[key])
