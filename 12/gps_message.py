from __future__ import annotations
import abc
import weakref
from dataclasses import dataclass
from math import radians, floor, fmod
from typing import (Optional, cast, Container, overload, Union, Sequence, Iterator)


class Buffer(Sequence[int]):
    def __init__(self, content: bytes) -> None:
        self.content = content

    def __len__(self) -> int:
        return len(self.content)
    
    def __iter__(self) -> Iterator[int]:
        return iter(self.content)
    
    @overload
    def __getitem__(self, index: int) -> int:
        ...

    @overload
    def __getitem__(self, index: slice) -> bytes:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[int, bytes]:
        return self.content[index]


class GPSError(Exception):
    pass


class Message:
    __slots__ = ("buffer", "offset", "end", "commas")

    def __init__(self) -> None:
        self.buffer: weakref.ReferenceType[Buffer]
        self.offset: int
        self.end: Optional[int]
        self.commas: list[int]

    def from_buffer(self, buffer: Buffer, offset: int) -> "Message":
        self.buffer = weakref.ref(buffer)
        self.offset = offset
        self.commas = [offset]
        self.end = None
        for index in range(offset, offset + 82):
            if buffer[index] == ord(b","):
                self.commas.append(index)
            elif buffer[index] == ord(b"*"):
                self.commas.append(index)
                self.end = index + 3
                break
        if self.end is None:
            raise GPSError("Incomplete")
        # TODO: confirm checksum.
        return self
    
    def __getitem__(self, field: int) -> bytes:
        if not hasattr(self, "buffer") or (buffer := self.buffer()) is None:
            raise RuntimeError("Broken reference")
        start, end = self.commas[field] + 1, self.commas[field + 1]
        return buffer[start:end]
    
    def get_fix(self) -> Point:
        return Point.from_bytes(
            self.latitude(), self.lat_n_s(), self.longitude(), self.lon_e_w
        )
    

class Point:
    __slots__ = ("latitude", "longitude")

    def __init__(self, latitude: float, longitude: float) -> None:
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self) -> str:
        return (
            f"Point(latitude={self.latitude}), "
            f"longitude={self.longitude}"
        )