"""
That module contains decorator that count time of function execution
"""
import logging
import time
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_time(func):
    """
    Decorator that count time of function execution
    """
    @wraps(func)
    def timer(*args, **kwargs):
        """
        Under decorator function
        """
        start_timer = time.perf_counter()

        try:
            result = func(*args, **kwargs)

        finally:
            end_timer = time.perf_counter()
            logger.info(
                "%s was executed by %.6f",
                func.__name__,
                end_timer - start_timer,
            )

        return result

    return timer
