from __future__ import annotations
from typing import *

import tcod
import numpy as np
from anathema.constants import SHEET_COLS, SHEET_ROWS

if TYPE_CHECKING:
    from numpy.typing import NDArray


class CharacterMap:

    def __init__(self) -> None:
        self._data: List[int] = tcod.tileset.CHARMAP_CP437
        _pua_start: int = 57344
        _pua_end: int = _pua_start + (32 * (SHEET_ROWS - 8))
        self._data.extend(range(_pua_start, _pua_end))
        self._shape = (32, len(self._data) // 32)

    @property
    def data(self) -> List[int]:
        return self._data

    @property
    def rows(self) -> int:
        return self._rows

    @rows.setter
    def rows(self, value: int) -> None:
        self._rows = value

    @property
    def as_array(self) -> NDArray[np.int]:
        return np.array(self._data, dtype=np.int).reshape(*self._shape).flat

    @property
    def enumerated(self) -> Generator[Tuple[int, int], None, None]:
        for count, value in enumerate(self._data):
            yield count, value
