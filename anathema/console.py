from __future__ import annotations
from typing import *
from contextlib import contextmanager

import tcod
import tcod.constants
from anathema.lib.morphism import (Rect, Point, Size)

import anathema.prepare as prepare

if TYPE_CHECKING:
    from anathema.typedefs import Color
    from numpy import ndarray


class Console:

    def __init__(self, console: tcod.console.Console) -> None:
        self._offset = Point(0, 0)
        self.console = console

    @property
    def root(self) -> tcod.console.Console:
        return self.console

    def set_fg(self, rect: Rect, value: Tuple[int, int, int]) -> None:
        computed = Rect(rect.origin + self._offset, rect.size)
        self.console.fg[
            computed.y:computed.y + computed.height,
            computed.x:computed.x + computed.width
        ] = value

    def set_bg(self, rect: Rect, value: Tuple[int, int, int]) -> None:
        computed = Rect(rect.origin + self._offset, rect.size)
        self.console.bg[
            computed.y:computed.y + computed.height,
            computed.x:computed.x + computed.width
        ] = value

    @contextmanager
    def translate(self, offset: Point) -> Generator[Point, Any, None]:
        previous = self._offset
        self._offset = self._offset + offset
        yield
        self._offset = previous

    def clear_area(self, rect: Rect, bg: Color = (21, 21, 21)) -> None:
        computed = Rect(rect.origin + self._offset, rect.size)
        self.draw_rect(
            computed,
            ch=32,
            fg=self.console.default_fg,
            bg=bg,
        )

    def draw_frame(
            self,
            rect: Rect,
            title: str = "",
            clear: bool = True,
            fg: Optional[Tuple[int, int, int]] = None,
            bg: Optional[Tuple[int, int, int]] = None,
            bg_blend: int = tcod.constants.BKGND_SET
        ) -> None:
        computed = Rect(rect.origin + self._offset, rect.size)
        self.console.draw_frame(
            computed.x,
            computed.y,
            computed.width,
            computed.height,
            title=title,
            clear=clear,
            fg=fg,
            bg=bg,
            bg_blend=bg_blend
        )

    def draw_rect(
            self,
            rect: Rect,
            ch: int,
            fg: Tuple[int, int, int] = (255, 255, 255),
            bg: Tuple[int, int, int] = (21, 21, 21),
            bg_blend: int = tcod.constants.BKGND_SET
        ) -> None:
        computed = Rect(rect.origin + self._offset, rect.size)
        self.console.draw_rect(
            computed.x,
            computed.y,
            computed.width,
            computed.height,
            ch=ch,
            fg=fg,
            bg=bg,
            bg_blend=bg_blend
        )

    def get_height_rect(self, rect: Rect, string: str) -> None:
        computed = Rect(rect.origin + self._offset, rect.size)
        self.console.get_height_rect(
            computed.x,
            computed.y,
            computed.width,
            computed.height,
            string=string,
        )

    def hline(self, point: Point, width: int, bg_blend: int = tcod.constants.BKGND_DEFAULT) -> None:
        computed = point + self._offset
        self.console.hline(int(computed.x), int(computed.y), width=width, bg_blend=bg_blend)

    def print(
            self,
            point: Point,
            string: str,
            fg: Optional[Tuple[int, int, int]] = None,
            bg: Optional[Tuple[int, int, int]] = None,
            bg_blend: int = tcod.constants.BKGND_SET,
            alignment: int = tcod.constants.LEFT,
        ) -> None:
        computed = point + self._offset
        self.console.print(
            int(computed.x),
            int(computed.y),
            string=string,
            fg=fg,
            bg=bg,
            bg_blend=bg_blend,
            alignment=alignment
        )

    def print_(
            self,
            point: Point,
            string: str,
            bg_blend: int = tcod.constants.BKGND_SET,
            alignment: int = tcod.constants.LEFT,
        ) -> None:
        computed = point + self._offset
        self.console.print_(
            int(computed.x),
            int(computed.y),
            string=string,
            bg_blend=bg_blend,
            alignment=alignment
        )

    def print_box(
            self,
            rect: Rect,
            string: str,
            fg: Optional[Tuple[int, int, int]] = None,
            bg: Optional[Tuple[int, int, int]] = None,
            bg_blend: int = tcod.constants.BKGND_SET,
            alignment: int = tcod.constants.LEFT,
        ) -> None:
        computed = Rect(rect.origin + self._offset, rect.size)
        self.console.print_box(
            computed.x,
            computed.y,
            computed.width,
            computed.height,
            string=string,
            fg=fg,
            bg=bg,
            bg_blend=bg_blend,
            alignment=alignment
        )

    def print_frame(
            self,
            rect: Rect,
            string: str = "",
            clear: bool = True,
            bg_blend: int = tcod.constants.BKGND_DEFAULT,
        ) -> None:
        computed = Rect(rect.origin + self._offset, rect.size)
        self.console.print_frame(
            computed.x,
            computed.y,
            computed.width,
            computed.height,
            string=string,
            clear=clear,
            bg_blend=bg_blend
        )

    def print_rect(
            self,
            rect: Rect,
            string: str,
            bg_blend: int = tcod.constants.BKGND_DEFAULT,
            alignment: Optional[int] = None
        ) -> None:
        computed = Rect(rect.origin + self._offset, rect.size)
        self.console.print_rect(
            computed.x,
            computed.y,
            computed.width,
            computed.height,
            string=string,
            bg_blend=bg_blend,
            alignment=alignment
        )

    def put_char(
            self,
            point: Point,
            ch: int,
            bg_blend: int = tcod.constants.BKGND_DEFAULT
        ) -> None:
        computed = point + self._offset
        self.console.put_char(int(computed.x), int(computed.y), ch=ch, bg_blend=bg_blend)

    def rect(
            self,
            rect: Rect,
            clear: bool,
            bg_blend: int = tcod.constants.BKGND_DEFAULT
        ) -> None:
        computed = Rect(rect.origin + self._offset, rect.size)
        self.console.rect(
            computed.x,
            computed.y,
            computed.width,
            computed.height,
            clear=clear,
            bg_blend=bg_blend
        )

    def vline(self, point: Point, height: int, bg_blend: int = tcod.constants.BKGND_DEFAULT) -> None:
        computed = point + self._offset
        self.console.vline(int(computed.x), int(computed.y), height=height, bg_blend=bg_blend)

    def tiles_rgb(self, point: Point, width: int, height: int) -> ndarray:
        computed = point + self._offset
        return cast(ndarray, self.console.tiles_rgb[computed.y:computed.y+height, computed.x:computed.x+width])


root_console = tcod.console.Console(*prepare.CONSOLE_SIZE)
root_console.bg[:] = (21, 21, 21)
console = Console(root_console)
