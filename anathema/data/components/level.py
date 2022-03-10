from __future__ import annotations
from typing import Tuple, Union

from anathema.lib.ecstremity import Component


class Level(Component):

    def __init__(self, value: int = 0) -> None:
        self.value = value
