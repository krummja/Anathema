from __future__ import annotations
from typing import Tuple, Any, TYPE_CHECKING, Optional, Callable

from morphism import Point, Size, Rect  # type: ignore
import tcod

from view import View
from anathema.views.label_view import LabelView

if TYPE_CHECKING:
    from tcod.event import KeyboardEvent
    from anathema.views.layout import Layout
    from anathema.screen import Screen


class ButtonView(View):
    """Contains a label. Can be first responder. When a button is the first
    responder:

    * The label is drawn black-on-white instead of white-on-black.
    * Pressing the ENTER key calls *callback*.
    """

    def __init__(
            self,

            # ButtonView parameters.
            text: str,
            callback: Callable[..., Optional[Any]],
            fg: Tuple[int, int, int] = (255, 255, 255),
            bg: Tuple[int, int, int] = (21, 21, 21),
            align_horz: str = 'center',
            align_vert: str = 'center',
            size: Optional[Size] = None,
            alt_fg: Tuple[int, int, int] | None = None,

            # Superview parameters.
            screen: Optional[Screen] = None,
            layout: Optional[Layout] = None,
            frame: Optional[Rect] = None,

        ) -> None:

        self.label_view = LabelView(
            text,
            align_horz=align_horz,
            align_vert=align_vert,
            size=size,
            fg=fg,
            bg=bg,
            )
        self.subviews = [self.label_view]
        super().__init__(screen, layout, self.subviews, frame)
        self.fg = fg
        self.bg = bg
        self.callback = callback
        self.alt = alt_fg

    def set_needs_layout(self, val: bool = True) -> None:
        super().set_needs_layout(val)
        self.label_view.set_needs_layout(val)

    def did_become_first_responder(self) -> None:
        if self.alt is not None:
            self.label_view.fg = self.alt
        else:
            self.label_view.fg = self.bg
            self.label_view.bg = self.fg

    def did_resign_first_responder(self) -> None:
        self.label_view.fg = self.fg
        self.label_view.bg = self.bg

    def draw(self) -> None:
        pass

    @property
    def text(self) -> str:
        return self.label_view.text

    @text.setter
    def text(self, new_value: str) -> None:
        self.label_view.text = new_value

    @property
    def intrinsic_size(self) -> Size:
        return self.label_view.intrinsic_size

    def layout_subviews(self) -> None:
        super().layout_subviews()
        self.label_view.frame = self.bounds

    @property
    def can_become_first_responder(self) -> bool:
        return True

    def handle_input(self, event: KeyboardEvent) -> bool:
        if self.callback:
            if event.sym == tcod.event.K_RETURN:
                self.callback()
                return True
        return False


class CyclingButtonView(ButtonView):

    def __init__(
            self,
            key: str,
            options: Any,
            initial_value: str,
            callback: Callable[..., Optional[Any]],
            fg: Tuple[int, int, int] = (255, 255, 255),
            bg: Tuple[int, int, int] = (21, 21, 21),
            align_horz: str = 'center',
            align_vert: str = 'center',
            size: Optional[Size] = None,
            screen: Optional[Screen] = None,
            layout: Optional[Layout] = None,
            frame: Optional[Rect] = None
        ) -> None:
        self.key = key
        self.options = options
        self._inner_callback = callback
        super().__init__(
            initial_value,
            self._call_inner_callback,
            fg, bg,
            align_horz, align_vert,
            size, screen, layout, frame
        )

    def _call_inner_callback(self) -> None:
        i = self.options.index(self.text)
        new_value = self.options[(i + 1) % len(self.options)]
        self.text = new_value
        self._inner_callback(self.key, new_value)
