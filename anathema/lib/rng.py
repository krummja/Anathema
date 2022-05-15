from __future__ import annotations
from typing import *

import random as rand

if TYPE_CHECKING:
    pass


def rand_float(min_or_max: Optional[float] = None, _max: Optional[float] = None) -> float:
    if not min_or_max:
        return rand.random()
    elif not _max:
        return rand.random() * min_or_max
    return rand.random() * (_max - min_or_max) + min_or_max


def random(min_or_max: int, _max: int | None = None) -> int:
    if _max is None:
        _max = min_or_max
        min_or_max = 0
    return rand.randrange(_max - min_or_max) + min_or_max


def one_in(chance: int) -> bool:
    return random(chance) == 0


def taper(start: int, chance_of_increment: int):
    while one_in(chance_of_increment):
        start += 1
    return start
