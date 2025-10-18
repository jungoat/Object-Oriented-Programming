from __future__ import annotations
import abc
import collections
import csv
import datetime
import itertools
import json
import jsonschema
from math import isclose
from pathlib import Path
import random
import sys
from typing import(
     cast,
     overload,
     Any,
     Optional,
     Union,
     Iterable,
     Iterator,
     List,
     Dict,
     Counter,
     Callable,
     Protocol,
     TypedDict,
     TypeVar,
     DefaultDict
)
import weakref
import vaml


class SamplePartition(List[SampleDict], abc.ABC):
    @overload
    def __init__(self,*,training_subset: float = 0.80) -> None:
        ...

    @overload
    def __init__(
        self,
        iterable: Optional[Iterable[SampleDict]] = None,
        *,
        training_subset: float = 0.80,
    ) -> None:
        ...

    def __init__(
            self,
            iterable: Optional[Iterable[SampelDict]] = None,
            *,
            training_subset: float = 0.80,
        ) -> None:
            self.training_subset = training_subset
            if iterable:
                 super().__init__(iterable)
            else:
                 super().__init__()
    
    @abc.abstractproperty
    @property
    def training(self) -> list[TrainingKnownSample]:
         ...

    @abc.abstractproperty
    @property
    def testing(self) -> list[TestingKnownSample]:
         ...

class SampleDict(TypedDict):
     sepal_length: float
     sepal_width: float
     petal_length: float
     petal_width: float
     species: str


class ShufflingSamplePartition(SamplePartition):
    def __init__(
        self,
        iterable: Optional[Iterable[SampleDict]] = None,
        *,
        training_subset: float = 0.80,
    ) -> None:
        super().__init__(iterable, training_subset=training_subset)
        self.split: Optional[int] = None

    def shuffle(self) -> None:
        if not self.split:
            random.shuffle(self)
            self.split = int(len(self) * self.training_subset)

    @property
    def training(self) -> list[TrainingKnownSample]:
         self.shuffle()
         return [TrainingKnownSample(**sd) for sd in self[: self.split]]
    
    @property
    def testing(self) -> list[TestingKnownSample]:
         self.shuffle()
         return [TestingKnwonSample(**sd) for sd in self[self.split :]]
    
ssp = ShufflingSamplePartition(training_subset = 0.67)
for row in data:
     ssp.append(row)

class DealingPartition(abc.ABC):
    @abc.abstractmethod
    def __init__(
        self,
        items: Optional[Iterable[SampleDict]],
        *,
        training_subset: tuple[int, int] = (8, 10),
    ) -> None:
        ...

    @abc.abstractmethod
    def extend(self, items: Iterable[SampleDict]) -> None:
        ...

    @abc.abstractmethod
    def append(self, item: SampleDict) -> None:
         ...

    @property
    @abc.abstractmethod
    def training(self) -> list[TrainingKnownSample]:
         ...
    
    @property
    @abc.abstractmethod
    def testing(self) -> list[TestingKnownSample]:
         ...

class CountingDealingPartition(DealingPartition):
    def __init__(
        self,
        items: Optional[Iterable[SampleDict]],
        *,
        training_subset: tuple[int, int] = (8, 10),
    ) -> None:
        self.training_subset = training_subset
        self.counter = 0
        self._training: list[TrainingKnownSample] = []
        self._testing: list[TestingKnownSample] = []
        if items:
            self.extend(items)

    def extend(self, items: Iterable[SampleDict]) -> None:
        for item in items:
            self.append(item)

    def append(self, item: SampleDict) -> None:
        n, d = self.training_subset
        if self.counter % d < n:
             self._training.append(TrainingKnownSample(**item))
        else:
             self._training.append(TestingKnownSample(**item))
        self.counter += 1

    @property
    def training(self) -> list[TrainingKnownSample]:
         return self._training
    
    @property
    def testing(self) -> lise[TestingKnownSample]:
         return self._testing
    
    
