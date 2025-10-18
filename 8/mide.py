from __future__ import annotations
from typing import (
    cast,
    Callable,
    Iterable,
    Iterator,
    List,
    NamedTuple,
    Optional,
    Type,
    Union,
)
from collections import defaultdict, Counter


class Sample(NamedTuple):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class KnownSample(NamedTuple):
    sample: Sample
    species: str


class TestingKnownSample(NamedTuple):
    sample: KnownSample

class TrainingKnownSample(NamedTuple):
    sample: KnownSample


def training_80(s: KnownSample, i: int) -> bool:
    return i % 5 != 0

def training_75(s: KnownSample, i: int) -> bool:
    return i % 4 != 0

def training_67(s: KnownSample, i: int) -> bool:
    return i % 3 != 0

TrainingList = List[TrainingKnownSample]
TestingList = List[TestingKnownSample]

def partition(
        samples: Iterable[KnownSample], rule: Callable[[KnownSample, int], bool]
)-> tuple[TrainingList, TestingList]:
    
    training_samples = [
        TrainingKnownSample(s) for i, s in enumerate(samples) if rule(s, i)
    ]

    test_samples = [
        TestingKnownSample(s) for i, s in enumerate(samples) if not rule(s, i)
    ]

    return training_samples, test_samples


def partition_1(
    samples: Iterable[KnownSample], rule: Callable[[KnownSample, int], bool]
) -> tuple[TrainingList, TestingList]:
    
    training: TrainingList = []
    testing: TestingList = []

    for i,s in enumerate(samples):
        training_use = rule(s,i)
        if training_use:
            training.append(TrainingKnownSample(s))
        else:
            testing.append(TestingKnownSample(s))

    return training, testing


def partition_1p(
        samples: Iterable[KnownSample], rule: Callable[[KnownSample, int], bool]
) -> tuple[TrainingList, TestingList]:
    
    pools: defaultdict[bool, list[KnownSample]] = defaultdict(list)
    partition = ((rule(s,i), s) for i, s in enumerate(samples))
    for usage_pool, sample in partition:
        pools[usage_pool].append(sample)

    training = [TrainingKnownSample(s) for s in pools[True]]
    testing = [TestingKnownSample(s) for s in pools[False]]
    return training, testing