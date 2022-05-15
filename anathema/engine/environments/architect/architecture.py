from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from .architectural_style import ArchitecturalStyle
    from .architect import Architect
    from .region import Region


class Architecture:

    def bind(self, style: ArchitecturalStyle, architect: Architect, region: Region) -> None:
        pass
