from __future__ import annotations

import re
from typing import *

import tcod

from anathema.data.components.noun import Pronoun
from anathema.gui.ui_colors import RESET

if TYPE_CHECKING:
    from anathema.typedefs import Color
    from anathema.data.components.noun import Noun
    from anathema.lib.ecstremity.component import Component


class Message:

    def __init__(
            self,
            text: str,
            noun1: Optional[Component] = None,
            noun2: Optional[Component] = None,
            noun3: Optional[Component] = None,
            color: Optional[Color] = None
        ) -> None:
        self.text = self._format(text, noun1=noun1, noun2=noun2, noun3=noun3)
        self.count = 1
        self.color = color

    def singular(self, text: str) -> str:
        return self._categorize(text, is_first = True)

    def conjugate(self, text: str, pronoun: Pronoun) -> str:
        if pronoun == Pronoun.you or pronoun == Pronoun.they:
            return self._categorize(text, is_first=True)
        return self._categorize(text)

    def quantify(self, text: str, count: int) -> str:
        pass

    def _format(
            self,
            text: str,
            noun1: Optional[Noun] = None,
            noun2: Optional[Noun] = None,
            noun3: Optional[Noun] = None
        ) -> str:
        result = text

        nouns = [noun1, noun2, noun3]
        for i, _ in enumerate(nouns):
            noun = nouns[i]
            if noun is not None:

                result = result.replace(f'{i}', noun.noun_text)

                result = result.replace(f"({noun.noun_text}, 'nom')", noun.pronoun().nom)
                result = result.replace(f"({noun.noun_text}, 'obl')", noun.pronoun().obl)
                result = result.replace(f"({noun.noun_text}, 'gen')", noun.pronoun().gen)

        if noun1 is not None:
            result = self.conjugate(result, noun1.pronoun)

        return result[0].upper() + result[1:]

    def _categorize(
            self,
            text: str,
            is_first: bool = False,
            force: bool = False
        ) -> str:
        assert is_first is not None

        optional_suffix = r"\[(\w+?)\]"
        irregular = r"\[([^|]+)\|([^\]]+)\]"

        # If it's a regular word in second category, add "s"
        if force and not is_first and text.find("[") != -1:
            return f"{text}s"

        # Handle words with optional suffixes like `close[s]` and `sword[s]`.
        while True:
            match = re.search(optional_suffix, text)
            if match is None:
                break

            before = text[0:match.span()[0]]
            after = text[match.span()[1]:]

            if is_first:
                text = f"{before}{after}"
            else:
                text = f"{before}{match[1]}{after}"

        # And now handle irregulars
        while True:
            match = re.search(irregular, text)
            if match is None:
                break

            before = text[0:match.span()[0]]
            after = text[match.span()[1]:]

            if is_first:
                text = f"{before}{match[1]}{after}"
            else:
                text = f"{before}{match[2]}{after}"

        return text

    def __str__(self) -> str:
        if self.count > 1:
            col = self.color if self.color else (255, 255, 255)
            return f"{tcod.COLCTRL_FORE_RGB:c}{col[0]:c}{col[1]:c}{col[2]:c}{self.text}{RESET} (x{self.count})"
        return self.text
