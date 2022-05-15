from __future__ import annotations
from typing import *

from math import floor, ceil

if TYPE_CHECKING:
    pass


def trunc_div(a: int, b: int) -> int:
    c = a / b
    return floor(c) if c > 0 else ceil(c)


def lerp_float(val: float, _min: float, _max: float, out_min: float, out_max: float) -> float:
    assert _min < _max
    if val <= _min:
        return out_min
    if val >= _max:
        return out_max
    t = (val - _min) / (_max - _min)
    return out_min + t * (out_max - out_min)

