from contextlib import contextmanager
import logging
from time import perf_counter
from datetime import timedelta
from fs.errors import ResourceNotFound


@contextmanager
def log_elapsed(ctx: str, log_lvl: int = logging.DEBUG, logger: logging.Logger = logging.getLogger("geovisio.utils")):
    """Context manager used to log the elapsed time of the context

    Args:
        ctx: Label to describe what is timed
        log_level: logging level, default to DEBUG
                logger: If set, use this logger to log, else the default logger is used
    """
    start = perf_counter()
    yield
    logger.log(log_lvl, f"{ctx} done in {timedelta(seconds=perf_counter()-start)}")


def removeFsEvenNotFound(fs, path):
    """Deletes file from given fs without raising ResourceNotFound exception"""
    try:
        fs.remove(path)
    except ResourceNotFound:
        pass


def removeFsTreeEvenNotFound(fs, path):
    """Deletes tree from given fs without raising ResourceNotFound exception"""
    try:
        fs.removetree(path)
    except ResourceNotFound:
        pass
