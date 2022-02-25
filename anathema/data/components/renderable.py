from __future__ import annotations
from typing import Tuple, Union

from anathema.lib.ecstremity import Component


class Renderable(Component):

    def __init__(self, char: Union[str, int], fg: Tuple[int, int, int]) -> None:
        if isinstance(char, str):
            self.char = ord(char)
        if isinstance(char, int):
            self.char = char
        self.fg = fg
