from typing import List

import fnmatch
import os
import sys

from setuptools import setup  # type: ignore
from setuptools.command.install import install  # type: ignore


modules: List[str] = []
matches: List[str] = []

for root, dirnames, filenames in os.walk('anathema'):
    for filename in fnmatch.filter(filenames, '__init__.py'):
        matches.append(os.path.join(root, filename))


for match in matches:
    match = match.replace(os.sep + "__init__.py", "")
    match = match.replace(os.sep, ".")
    modules.append(match)


setup(
    name="Anathema",
    version="1.0.0",
    url="https://www.github.com/krummja/Anathema",
    author="Jonathan Crum",
    license="MIT",
    packages=modules,
    entry_points={
      'gui_scripts': [
          'anathema = anathema.__main__:main'
      ]
    },
    zip_safe="false"
)
