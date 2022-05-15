from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    pass


class QueryKey:

    def __init__(self, name: str, depth: int) -> None:
        self.name = name
        self.depth = depth

    def __hash__(self) -> int:
        return hash(self.name) ^ hash(self.depth)

    def __eq__(self, other: object) -> None:
        query = cast(QueryKey, other)
        return self.name == query.name and self.depth == other.depth

    def __str__(self) -> str:
        return f"{self.name} ({self.depth})"
