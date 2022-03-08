import logging
import sys

from anathema import prepare
from print_utils import bcolors, cprint


def configure() -> None:
    """Configure logging based on the settings in the config file."""

    LOG_LEVELS = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }
    config = prepare.CONFIG
    loggers = {}

    if config.debug_level in LOG_LEVELS:
        log_level = LOG_LEVELS[config.debug_level]
    else:
        log_level = logging.INFO

    if config.debug_logging:
        for logger_name in config.loggers:

            if logger_name == "all":
                print(f"Enabling logging of all modules [{log_level}] \n")
                logger = logging.getLogger()
            else:
                print(f"Enabling logging for module: {logger_name} [{log_level}] \n")
                logger = logging.getLogger(logger_name)

            logger.setLevel(log_level)
            log_handler = logging.StreamHandler(sys.stdout)
            log_handler.setLevel(log_level)

            if log_level >= 30:
                log_color = bcolors.FAIL
            elif log_level >= 20:
                log_color = bcolors.WARNING
            else:
                log_color = bcolors.HEADER

            mod_string = cprint(log_color, "%(module)-8s")  + " :: "
            level_string = cprint(log_color, "%(levelname)-8s")  + " :: "
            formatter = logging.Formatter(mod_string + level_string + "%(message)s")

            log_handler.setFormatter(formatter)
            logger.addHandler(log_handler)
            loggers[logger_name] = logger
