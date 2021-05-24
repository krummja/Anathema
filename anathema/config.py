from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional, Tuple

import configparser
from collections import OrderedDict
import tcod

if TYPE_CHECKING:
    from configparser import ConfigParser


class AnathemaConfig:

    def __init__(self, config_path: Optional[str] = None) -> None:
        cfg = generate_default_config()
        self.cfg = cfg

        if config_path:
            temp = configparser.ConfigParser()
            temp.read(config_path)
            populate_config(cfg, temp._sections)  # type: ignore

        # [display]
        console_width = cfg.getint("display", "console_width")
        console_height = cfg.getint("display", "console_height")
        self.console_dims = console_width, console_height
        self.tileset = cfg.get("display", "tileset")
        self.window_name = cfg.get("display", "window_name")
        self.vsync = cfg.getboolean("display", "vsync")

        # [game]
        self.data = cfg.get("game", "data")
        self.starting_zone = cfg.get("game", "starting_zone")
        self.zone_size = cfg.getint("game", "zone_size")
        self.debug = cfg.get("game", "debug")

        # [interface]
        self.stage_panel_width = cfg.getint("interface", "stage_panel_width")
        self.stage_panel_height = cfg.getint("interface", "stage_panel_height")

        # [logging]
        loggers = cfg.get("logging", "loggers")
        self.loggers = loggers.replace(" ", "").split(",")
        self.debug_logging = cfg.getboolean("logging", "debug_logging")
        self.debug_level = cfg.get("logging", "debug_level")


def get_defaults() -> OrderedDict[str, Any]:
    return OrderedDict(
        (
            (
                "display",
                OrderedDict(
                    (
                        ("console_width", 110),
                        ("console_height", 65),
                        ("tileset", "font_16.png"),
                        ("window_name", "Anathema"),
                        ("vsync", True),
                    )
                )
            ),
            (
                "game",
                OrderedDict(
                    (
                        ("data", "anathema"),
                        ("starting_zone", "dev_starting_zone"),
                        ("zone_size", 512),
                        ("debug", False)
                    )
                )
            ),
            (
                "interface",
                OrderedDict(
                    (
                        ("stage_panel_width", 72),
                        ("stage_panel_height", 50)
                    )
                )
            ),
            (
                "logging",
                OrderedDict((("loggers", "all"), ("debug_logging", True), ("debug_level", "error")))
            ),
        )
    )


def generate_default_config() -> ConfigParser:
    """Get new config file from defaults."""
    cfg = configparser.ConfigParser()
    populate_config(cfg, get_defaults())
    return cfg


def populate_config(config: ConfigParser, data: OrderedDict[str, Any]) -> None:
    for k, v in data.items():
        try:
            config.add_section(k)
        except configparser.DuplicateSectionError:
            pass
        for option, value in v.items():
            config.set(k, option, str(value))
