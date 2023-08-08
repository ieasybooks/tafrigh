import time
from functools import wraps
from typing import Callable, TypeVar

T = TypeVar("T", bound=Callable)


def minimum_execution_time(minimum_time: float) -> Callable[[T], T]:
    def decorator(func: T) -> T:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

            elapsed_time = end_time - start_time
            if elapsed_time < minimum_time:
                time.sleep(minimum_time - elapsed_time)

            return result

        return wrapper

    return decorator
