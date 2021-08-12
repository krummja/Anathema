from __future__ import annotations
from typing import Tuple, Optional
from anathema.engine.environments.tile_type import TileType
from anathema.constants.color import Color


def tile(
        name: str,
        char: str,
        fore: Tuple[int, int, int],
        back: Optional[Tuple[int, int, int]] = None
    ) -> TileType:
    return TileType(name, char, fore, back if back else (21, 21, 21))


class Tiles:
    unformed = tile("unformed", "?", Color.light_cool_gray).open()
    unformed_wet = tile("unformed_wet", "≈", Color.light_blue).open()
    open_ground = tile("open", ".", Color.white).open()
    solid = tile("solid", "#", Color.light_cool_gray).solid()
    passage = tile("passage", "-", Color.light_cool_gray).open()
    solid_wet = tile("solid_wet", "≈", Color.cool_gray).obstacle()
    passage_wet = tile("passage_wet", "≈", Color.light_blue).open()
    doorway = tile("doorway", "○", Color.light_cool_gray).open()

    flagstone_wall = tile("Flagstone Wall", "▒", Color.light_warm_gray, Color.warm_gray).solid()
    granite_wall = tile("Granite Wall", "▒", Color.cool_gray).solid()
    granite_1 = tile("Granite", "▓", Color.dark_cool_gray).solid()

    flagstone_floor = tile("Flagstone Floor", ".", Color.warm_gray, Color.dark_warm_gray).open()
    granite_floor = tile("Granite Floor", ".", Color.dark_cool_gray, Color.darker_cool_gray).open()

    dirt_1 = tile("Dirt", "·", Color.brown).open()
    dirt_2 = tile("Dirt", "φ", Color.brown).open()
    grass = tile("Grass", "░", Color.lima).open()
    tall_grass = tile("Tall Grass", "√", Color.pea_green).obfuscated()
    tree_1 = tile("Evergreen Tree", "▲", Color.sherwood).solid()
    shallow_water = tile("Shallow Water", "≈", Color.light_blue).open()
