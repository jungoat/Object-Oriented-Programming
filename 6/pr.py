from __future__ import annotations
from collections import abc
from typing import Protocol, Any, overload, Union
import bisect
from typing import Iterator, Iterable, Sequence, Mapping


class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool:
        ...

    def __ne__(self, other: Any) -> bool:
        ...

    def __le__(self, other: Any) -> bool:
        ...

    def __lt__(self, other: Any) -> bool:
        ...

    def __ge__(self, other: Any) -> bool:
        ...

    def __gt__(self, other: Any) -> bool:
        ...


import sys

if sys.version_info >= (3, 9):
    BaseMapping = abc.Mapping[Comparable, Any]
else:
    BaseMapping = Mapping[Comparable, Any]


class Lookup(BaseMapping):
    @overload
    def __init__(self, source: Iterable[tuple[Comparable,Any]]) -> None:
        ...

    def __init__(
        self,
        source: Union[Iterable[tuple[Comparable, Any]], BaseMapping, None] = None,
    ) -> None:
        sorted_pairs : Sequence[tuple[Comparable, Any]]
        if isinstance(source, Sequence):
            sorted_pairs = sorted(source)
        elif isinstance(source, abc.Mapping):
            sorted_pairs = sorted(source.items())
        else:
            sorted_pairs = []
        self.key_list = [p[0] for p in sorted_pairs]
        self.value_list = [p[1] for p in sorted_pairs]

    def __len__(self) -> int:
        return len(self.key_list)
    
    def __iter__(self) -> Iterator[Comparable]:
        return iter(self.key_list)
    
    def __contains__(self, key: object) -> bool:
        index = bisect.bisect_left(self.key_list, key)
        return key == self.key_list[index]
    
    def __getitem__(self, key: Comparable) -> Any:
        index = bisect.bisect_left(self.key_list, key)
        if key == self.key_list[index]:
            return self.value_list[index]
        raise KeyError(key)
    
    