len([1,2,3,4])

class CustomSequence:
    def __init__(self, args):
        self._list = args

    def __len__(self):
        return 5
    
    def __getitem__(self, index):
        return f"x{index}"
    
class FunkyBackwards(list):
    def __reversed__(self):
        return "BACKWARDS!"

generic = [1, 2, 3, 4, 5]
custom = CustomSequence([6, 7, 8, 9, 10])
funkadelic = FunkyBackwards([11, 12, 13, 14, 15])

for sequence in generic, custom, funkadelic:
    print(f"{sequence.__class__.__name__}: ", end="")
    for item in reversed(sequence):
        print(f"{item}, ", end="")
    print()

from pathlib import Path
with Path("docs/sample_data.md").open() as source:
    for index, line in enumerate(source, start=1):
        print(f"{index:3d}: {line.rstrip()}")

def no_params():
    return "Hello, world!"

no_params

def mandatory_params(x, y, z):
    return f"{x=}, {y=}, {z=}"

a_variable = 42
mandatory_params("a string", a_variable, True)

from typing import Any, Optional

def mandatory_params(x: Any, y: Any, z: Any) -> str:
    return f"{x=}, {y=}, {z=}"

def latitude_dms(
    deg: float, min: float, sec: float = 0.0, dir: Optional[str] = None
) -> str:
    if dir is None:
        dir = "N"
    return f"{deg:02.0f}° {min+sec/60:05.3f}{dir}"

def kw_only(x: Any, y: str = "defaultkw", *, a: bool, b: str = "only") -> str:
    return f"{x=}, {y=}, {a=}, {b=}"

def pos_only(x: Any, y: str, / , z: Optional[Any] = None) -> str:
    return f"{x=}, {y=}, {z=}"

test_pos_only = """"""

number = 5

def funky_function(x: int = number) -> str:
    return f"{x=}, {number=}"

def better_function(x: Optional[int] = None) -> str:
    if x is None:
        x = number
    return f"bertter: {x=}, {number=}"

def better_function2(x: Optional[int] = None) -> str:
    x = number if x is None else x
    return f"better: {x=}, {number=}"

from typing import List

def bad_default(tag:str, history: list[str] = []) -> list[str]:
    history.append(tag)
    return history

def good_default(tag: str, history: Optional[list[str]] = None) -> list[str]:
    history = [] if history is None else history
    history.append(tag)
    return history

from urllib.parse import urlparse
from pathlib import Path

def get_pages(*links: str) -> None:
    for link in links:
        url = urlparse(link)
        name = "index.html" if url.path in ("","/") else url.path
        target = Path(url.netloc.replace(".","_")) / name
        print(f"Create {target} from {link!r}")


from typing import Dict, Any


class Options(Dict[str, Any]):
    default_options: dict[str, Any] = {
        "port": 21,
        "host": "localhost",
        "username" : None,
        "password" : None,
        "debug" : False,
                }
    
    def __init__(self, **kwargs: Any) -> None:
        super().__init__({**self.default_options, **kwargs})


import contextlib
import os
import subprocess
import sys
from typing import TextIO
from pathlib import Path


def doctest_everything(
        outpit: TextIO, *directories: Path, verbose: bool = False, **stems: str
)-> None:
    def log(*args: Any, **kwargs: Any) -> None:
        if verbose:
            print(*args, **kwargs)

    with contextlib.redirect_stdout(output):
        for directory in directories:
            log(f"Searching {directory}")
            for path in directory.glob("**/*.md"):
                if any(parent.stem == ".tox" for parent in path.parents):
                    continue
                log(f"File {path.relative_to(directory)}, " f"{path.stem=}")
                if stems.get(path.stem, "").upper() == "SKIP":
                    log("Skipped")
                    continue
                options = []
                if stems.get(path.stem, "").upper() == "ELLIPSIS":
                    options += ["ELLIPSIS"]
                search_path = directory / "src"
                print(
                    f"cd '{Path.cwd()}'; "
                    f"PYTHONPATH= '{search_path}' doctest '{path}' -v"
                )
                options_args = ["-o", ",".join(options)] if options else []
                subprocess.run(
                    ["python3", "-m", "doctests", "-v"] + options_args + [str(path)],
                    cwd=directory,
                    env={"PYTHONPATH": str(search_path)},
                )

def show_args(arg1, arg2, arg3="THREE"):
    return f"{arg1=}, {arg2=}, {arg3=}"

some_args = range(3)
show_args(*some_args)

def __init__(self, **kwargs: Any) -> None:
    super().__init__(self.default_options)
    self.update(kwargs)

def __init__(self, **kwargs: Any) -> None:
    super().__init__({**self.default_options, **kwargs})