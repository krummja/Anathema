from __future__ import annotations
from typing import *

import numpy as np
import tcod


class CharacterMap:

    def __init__(self) -> None:
        self._data: List[int] = tcod.tileset.CHARMAP_CP437
        _pua_start: int = 57344
        _pua_end: int = 57856
        self._data.extend(range(_pua_start, _pua_end))
