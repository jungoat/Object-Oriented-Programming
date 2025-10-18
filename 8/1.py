from __future__ import annotations
from typing import Any, Optional


def no_params() -> str:
    return "Hello, world!"


from typing import Any


def mandatory_params(x: Any, y: Any, z: Any) -> str:
    return f"{x=}, {y=}, {z=}"




def default_params(
    x: Any, y: Any, z: Any, a: str = "Some String", b: bool = False
) -> str:
    return f"{x=}, {y=}, {z=}, {a=}, {b=}"
    pass



def latitude_dms(
    deg: float, min: float, sec: float = 0.0, dir: Optional[str] = None
) -> str:
    if dir is None:
        dir = "N"
    return f"{deg:02.0f}° {min+sec/60:05.3f}{dir}"




def kw_only(x: Any, y: str = "defaultkw", *, a: bool, b: str = "only") -> str:
    return f"{x=}, {y=}, {a=}, {b=}"





def pos_only(x: Any, y: str, /, z: Optional[Any] = None) -> str:
    return f"{x=}, {y=}, {z=}"


number = 5


def funky_function(x: int = number) -> str:
    return f"{x=}, {number=}"

def better_function(x: Optional[int] = None) -> str:
    if x is None:
        x = number
    return f"better: {x=}, {number=}"


def better_function(x: Optional[int] = None) -> str:
    x = number if x is None else x
    return f"better: {x=}, {number=}"


from typing import List

def bad_default(tag: str, history: list[str] = []) -> list[str]:
    history.append(tag)
    return history

from urllib.parse import urlparse
from pathlib import Path


def get_pages(*links: str) -> None:
    for link in links:
        url = urlparse(link)
        name = "index.html" if url.path in ("", "/") else url.path
        target = Path(url.netloc.replace(".", "_")) / name
        print(f"Create {target} from {link!r}")


from __future__ import annotations
import contextlib
import os
import subprocess
import sys
from typing import TextIO

def doctest_everything(
        output: TextIO, *directories: Path, verbose: bool = False, **stems: str
) -> None:
    def log(*args: Any, **kwargs: Any) -> None:
        if verbose:
            print(*args, **kwargs)

    with contextlib.redirect_stdout(output):
        for directory in directories

with open("a.text") as input:
    for line in input:
        print(line)


class StringJoiner(List[str]):
    def __enter__(self) -> "StringJoiner":
        return self
    
    def __exit__(
            self,
            exc_type
    )