from __future__ import annotations
import collections
from dataclasses import dataclass, asdict
from typing import Optional, Counter, List
import weakref
import sys


@dataclass
class Sample:
    sepla_length: float
    sepla_width: float
    petal_length: float
    petal_width: float


@dataclass
class KnownSample(Sample):
    species: str


@dataclass
class TestingKnownSample(KnownSample):
    classification: Optional[str] = None


@dataclass
class TestingKnownSample(KnownSample):
    pass


@dataclass
class Distance:
    def distance(self, s1: Sample, s2: Sample) -> float:
        raise NotImplementedError
    

@dataclass
class Hyperparameter:
    k: int
    algorithm: Distance
    data: weakref.ReferenceType["TrainingData"]

    def classify(self, sample: Sample) -> str:
        if not (training_data := self.data()):
            raise RuntimeError("NO Training object")
        distances: list[tuple[float, TrainingKnownSample]] = sorted(
            (self.algorithm.distance(sample, known), known)
            for known in training_data.training
        )

import collections
from typing import Optional, Counter, NamedTuple
import weakref
import sys


class Sample(NamedTuple):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class KnownSample(NamedTuple):
    sample: Sample
    species: str


class TestingKnownSample:
    def __init__(
            self, sample: KnownSample, classification: Optional[str] = None
    ) -> None:
        self.sample = sample
        self.classification = classification

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(sample={self.sample!r},"
            f"classification={self.classification!r})"
        )
    

class CustomSequence:
    def __init__(self, args):
        self._list = args

    def __len__(self):
        return 5
    
    def __getitem__(self, index):
        return f"x{index}"
    

from pathlib import Path
with Path("docs/sample_data.md").open() as source:
    for index, line in enumerate(source, start=1):
        print(f"{index:3d}: {line.rstrip()}")