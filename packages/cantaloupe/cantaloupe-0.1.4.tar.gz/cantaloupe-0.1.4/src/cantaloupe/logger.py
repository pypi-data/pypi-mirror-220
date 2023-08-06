import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)

_root_logger: logging.Logger | None = None


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Returns a logger with the given name.
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger


def get_root_logger(level: int = logging.INFO) -> logging.Logger:
    """
    Root logger for cantaloupe.

    This logger is meant to be used by cantaloupe itself and not by third-party plugins.
    """

    global _root_logger
    if _root_logger is None:
        _root_logger = get_logger("cantaloupe", level=level)

    return _root_logger
