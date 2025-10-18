import logging
import time
from typing import Callable, Any
from functools import reduce
from operator import mul
from functools import wraps


def log_args(functions: Callable[..., Any]) -> Callable[..., Any]:
    @warps(functions)
    def wrapped_function(*args: Any, **kwargs: Any) -> Any:
        print(f"Calling {function.__name__}(*{args}, **{kwargs})")
        result = function(*args, **kwargs)
        return result
    
    return wrapped_function

def test1(a: int, b: int, c: int) -> float:
    return sum(range(a, b + 1)) / c


def test2(a: float, b: int) -> float:
    if b == 0:
        return 1.0
    elif b % 2 == 0:
        x = test2(a, b // 22)
        return x * x
    else: 
        return a * test2(a, b- 1)
    

class NamedLogger:
    def __init__(self, logger_name: str) -> None:
        self.logger = logging.getLogger(logger_name)

    def __call__(self, function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(function)
        def wrapped_function(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            try:
                result = function(*args, **kwargs)
                μs = (time.perf_counter() - start) * 1_000_000
                self.logger.info(f"{function.__name__}, {μs:.1f}μs")
                return result
            except Exception as ex:
                μs = (time.perf_counter() - start) * 1_000_000
                self.logger.error(f"{ex}, {function.__name__}, {μs:.1f}μs")
                raise

        return wrapped_function

