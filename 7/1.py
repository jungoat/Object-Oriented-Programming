from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Stock:
    symbol: str
    current: float
    high: float
    low: float


class StockOrdinary:
    def __init__(self, name: str, current: float, high: float, low: float) -> None:
        self.name = name
        self.current = current
        self.high = high
        self.low = low

s_ord = StockOrdinary("AAPL", 123.52, 137.98, 53.15)


@dataclass
class StockDefaults:
    name: str = 0.0
    current: float = 0.0
    high: float = 0.0
    low: float = 0.0

for stock, values in stocks.items():
    print(f"{stock} last value is {values[0]}")
    

def letter_frequency_2(sentence: str) -> defaultdict[str, int]:
    frequencies: defaultdict[str, int] = defaultdict(int)
    for letter in sentence:
        frequencies[letter] += 1
    return frequencies


from collections import Counter

def letter_frequency_3(sentence: str) -> Counter[str]:
    return Counter(sentence)


from __future__ import annotations
import string

CHARACTERS = list(string.ascii_letters) + [" "]


def letter_frequency(sentence: str) -> list[tuple[str, int]]:
    frequencies = [(c, 0) for c in CHARACTERS]
    for letter in sentence:
        index = CHARACTERS.index(letter)
        frequencies[index] = (letter, frequencies[index][1] + 1)
    non_zero = [(letter, count) for letter, count in frequencies if count > 0]
    return non_zero


from typing import Optional, cast, Any
from dataclasses import dataclass
import datetime
from datetime import timezone


@dataclass(frozen=True)
class MultiItem:
    data_source: str
    timestamp: Optional[float]
    creation_date: Optional[str]
    name: str
    owner_etc: str

    def __lt__(self, other: Any) -> bool:
        if self.data_source == "Local":
            self_datetime = datetime.datetime.fromtimestamp(
                cast(float, self.timestamp), tz=timezone.utc
            )
        else:
            self_datetime = datetime.datetime.fromisoformat(
                cast(str, self.creation_date)
            ).replace(tzinfo=timezone.utc)

@dataclass
class SimpleMultiItem:
    data_source: str
    timestamp: Optional[float]
    creation_date: Optional[str]
    name: str
    owner_etc: str

def by_timestamp(item: SimpleMultiItem) -> datetime.datetime:
    if item.data_source == "Local":
        return datetime.datetime.fromtimestamp(
            cast(float, item.timestamp), tz=timezone.utc
        )
    elif item.data_source == "Remote":
        return datetime.datetime.fromisoformat(cast(str, item.creation_date)).replace(
            tzinfo=timezone.utc
        )
    else:
        raise ValueError(f"Unknown data_source in {item!r}")
    

from __future__ import annotations
import abc
from pathlib import Path
from typing import cast, Type, Union, List
import time


class DirectoryVisitor(abc.ABC):
    queue_class: Type["PathQueue"]

    def __init__(self, base: Path) -> None:
        self.queue = self.queue_class()
        self.queue.put(base)

    @abc.abstractmethod
    def file(self, path: Path) -> None:
        print(path)

    def visit(self) -> None:
        while not self.queue.empty():
            item = self.queue.get()
            if item.is_file():
                self.file(item)
            elif item.is_dir():
                if item.name.startswith("."):
                    continue
                if item.name == "__pycache__":
                    continue
                for sub_item in item.iterdir():
                    self.queue.put(sub_item)

class ListQueue(List[Path]):
    def put(self, item: Path) -> None:
        self.append(item)

    def get(self) -> Path:
        return self.pop(0) 
    
    def empty(self) -> bool:
        return len(self) == 0
    
import queue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    BaseQueue = queue.Queue[Path]
else:
    BaseQueue = queue.Queue

    