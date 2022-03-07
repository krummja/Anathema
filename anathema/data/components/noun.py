from __future__ import annotations
from typing import TYPE_CHECKING, Tuple
import numpy as np

from anathema.lib.ecstremity import Component

if TYPE_CHECKING:
    from numpy.lib.index_tricks import IndexExpression


class Noun(Component):

    def __init__(self, text: str) -> None:
        self._noun_text: str = text

    @property
    def noun_text(self):
        return self._noun_text

    @property
    def pronoun(self):
        return Pronoun.it


class Pronoun:
    """Representation of a pronoun."""

    nom: str
    obl: str
    gen: str

    def __init__(self, nom: str, obl: str, gen: str) -> None:
        self.nom = nom
        self.obl = obl
        self.gen = gen

    @classmethod
    def you(cls) -> Pronoun:
        return Pronoun('you', 'you', 'your')

    @classmethod
    def she(cls) -> Pronoun:
        return Pronoun('she', 'her', 'her')

    @classmethod
    def he(cls) -> Pronoun:
        return Pronoun('he', 'him', 'his')

    @classmethod
    def it(cls) -> Pronoun:
        return Pronoun('it', 'it', 'its')

    @classmethod
    def they(cls) -> Pronoun:
        return Pronoun('they', 'them', 'their')
