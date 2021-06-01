from __future__ import annotations
from typing import Tuple

# type: Component
from ecstremity import Component


class Renderable(Component):

    def __init__(self, char: str, fg: Tuple[int, int, int]) -> None:
        self.char = ord(char)
        self.fg = fg
