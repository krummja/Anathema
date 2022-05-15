from __future__ import annotations
from typing import *

from . import T

if TYPE_CHECKING:
    pass


class Tag(Generic[T]):

    def __init__(self, name: str, parent: Optional[Tag[T]]) -> None:
        self.name = name
        self.parent = parent

    def contains(self, tag: Tag[T]) -> bool:
        if tag == self:
            return True
        while self.parent:
            return self.parent.contains(tag)
        return False

    def __str__(self):
        if self.parent is None:
            return self.name
        return f"{self.parent}/{self.name}"
