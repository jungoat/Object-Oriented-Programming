from __future__ import annotations
import collections
import datetime
from math import isclose
from typing import (cast, Optional, Union, Iterator, Iterable, Counter, Callable, Protocol,)
import weakref


row = {"sepal_lenght": "5.1", "sepal_width": "3.5", "petal_lenght" : "1.4", "petal_width" : "0.2", "species" : "Iris-setosa"}

class InvalidSampleError(ValueError):
    pass

class Sample:
    def __init__(
        self,
        sepal_length: float,
        sepal_width: float,
        petal_length: float,
        petal_width: float,
    ) -> None:
        self.sepal_length = sepal_length
        self.sepal_width = sepal_width
        self.petal_length = petal_length
        self.petal_width = petal_width

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"sepal_length={self.sepal_length}, "
            f"sepal_width={self.sepal_width}, "
            f"petal_length={self.petal_length}, "
            f"petal_width={self.petal_width}, "
            f")"
        )


class KnownSample(Sample):
    def __init__(
        self,
        species: str,
        sepal_length: float,
        sepal_width: float,
        petal_length: float,
        petal_width: float,
    ) -> None:
        super().__init__(
            sepal_length=sepal_length,
            sepal_width=sepal_width,
            petal_length=petal_length,
            petal_width=petal_width,
        )
        self.species = species

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"sepal_length={self.sepal_length}, "
            f"sepal_width={self.sepal_width}, "
            f"petal_length={self.petal_length}, "
            f"petal_width={self.petal_width}, "
            f"species={self.species!r}, "
            f")"
        )
    
    @classmethod
    def from_dict(cls, row: dict[str, str]) -> "KnownSample":
        if row["species"] not in {
            "Iris-setosa", "Iris-versicolour", "Iris-virginica"}:
            raise InvalidSampleError(f"invalid species in {row!r}")
        try:
            return cls(
                species=row["species"],
                sepal_length=float(row["sepal_length"]),
                sepal_width=float(row["sepal_width"]),
                petal_lenght=float(row["petal_length"]),
                petal_width=float(row["petal_width"])       
                )
        except ValueError as ex:
            raise InvalidSampleError(f"invalid {row!r}")

class TrainingKnownSample(KnownSample):
    @classmethod
    def from_dict(cls, row: dict[str, str]) -> "TrainingKnownSample":
        return cast(TrainingKnownSample, super().from_dict(row))

class TestingKnownSample(KnownSample):
    def __init__(
        self,
        /,
        species: str,
        sepal_length: float,
        sepal_width: float,
        petal_length: float,
        petal_width: float,
        classification: Optional[str] = None,
    ) -> None:
        super().__init__(
            species=species,
            sepal_length=sepal_length,
            sepal_width=sepal_width,
            petal_length=petal_length,
            petal_width=petal_width,
        )
        self.classification = classification

    def matches(self) -> str:
        return (
            f"{self.__class__.__name__}"
        )
    
    def __repr__(self) -> str:
        return(
            f"{self.__class__.__name__}("
            f"sepal_length={self.sepal_length}, "
            f"sepal_width={self.sepal_width}, "
            f"petal_length={self.petal_length}, "
            f"petal_width={self.petal_width}, "
            f"species={self.species!r}, "
            f"classification={self.classification!r}, "
            f")"
        )
    
    @classmethod
    def from_dict(cls, row: dict[str, str]) -> "TestingKnownSample":
        return cast(TestingKnownSample, super().from_dict(row))

from enum import Enum
class Species(Enum):
    Setosa = "Iris-setosa"
    Versicolour = "Iris-versicolour"
    Viginica = "Iris-virginica"

Species("Iris-setosa")

Species("Iris-pinniped")

from typing import Set
class Domain(Set[str]):
    def validate(self, value: str) -> str:
        if value in self:
            return value
        raise ValueError(f"invalid {value!r}")
species = Domain({"Iris-setosa", "Iris-versicolour", "Iris-virginica"})
species.validate("Iris-versicolour")
species.validate("odobenidae")

class TrainingData:

    def __init__(self, name: str) -> None:
        self.name = name
        self.uploaded: datetime.datetime
        self.tested: datetime.datetime
        self.training: list[TrainingKnownSample] = []
        self.testing: list[TestingKnownSample] = []
        self.tuning: list[Hyperparameter] = []
'''
    def load(self, raw_data_iter: Iterable[dict[str, str]]) -> None:
        for n, row in enumerate(raw_data_iter):
            try:
                if n % 5 == 0:
                    test = TestingKnownSample.from_dict(row)
                    self.testing.apped(test)
                else:
                    train = TrainingKnownSample.from_dict(row)
                    self.training.append(train)
            except InvalidSampleError as ex:
                print(f"Row {n+1}: {ex}")
                return
        self.uploaded = datetime.datetime.now(tz=datetime.timezone.utc)
'''
def load(self, raw_data_iter: Iterable[dict[str, str]]) -> None:
    bad_count = 0
    for n, row in enumerate(raw_data_iter):
        try:
            if n % 5 == 0:
                test = TestingKnownSample.from_dict(row)
                self.testing.apped(test)
            else:
                train = TrainingKnownSample.from_dict(row)
                self.training.append(train)
        except InvalidSampleError as ex:
            print(f"Row {n+1}: {ex}")
            bad_count += 1
    if bad_count != 0:
        print(f"{bad_count} invalid rows")
        return
    self.uploaded = datetime.datetime.now(tz=datetime.timezone.utc)