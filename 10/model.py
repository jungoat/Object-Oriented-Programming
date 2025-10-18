"""
Python 3 Object-Oriented Programming Case Study

Chapter 10. The Iterator Pattern
"""
from __future__ import annotations
import bisect
import heapq
import collections
from typing import cast, NamedTuple, Callable, Iterable, List, Union, Counter


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


TestingList = List[TestingKnownSample]
TrainingList = List[TrainingKnownSample]


class UnknownSample(NamedTuple):
    sample: Sample


class ClassifiedKnownSample(NamedTuple):
    sample: KnownSample
    classification: str


class ClassifiedUnknownSample(NamedTuple):
    sample: UnknownSample
    classification: str


AnySample = Union[KnownSample, UnknownSample]
DistanceFunc = Callable[[TrainingKnownSample, AnySample], float]


class Measured(NamedTuple):
    """Measured distance is first to simplify sorting."""

    distance: float
    sample: TrainingKnownSample



import itertools
from typing import DefaultDict, Tuple, Iterator

ModuloDict = DefaultDict[int, list[KnownSample]]


def partition_2(
        samples: Iterable[KnownSample], training_rule: Callable[[int], bool]
) -> tuple[TrainingList, TestingList]:
    rule_mutiple = 60
    partitions: ModuloDict = collections.defaultdict(list)
    for s in samples:
        partitions[hash(s) % rule_mutiple].append(s)

    training_partitions: list[Iterator[TrainingKnownSample]] = []
    testing_partitions: list[Iterator[TestingKnownSample]] = []
    for i, p in enumerate(partitions.values()):
        if training_rule(i):
            training_partitions.append(TrainingKnownSample(s) for s in p)
        else:
            testing_partitions.append(TestingKnownSample(s) for s in p)

    training = list(itertools.chain(*training_partitions))
    testing = list(itertools.chain(*testing_partitions))  
    return training, testing 


Classifier = Callable[[int, DistanceFunc, TrainingList, AnySample], str]


class Hyperparameter(NamedTuple):
    k: int
    distance_function: DistanceFunc
    training_data: TrainingList
    classifier: Classifier

    def classify(self, unknown: AnySample) -> str:
        classifier = self.classifier
        return classifier(self.k, self.distance_function, self.training_data, unknown)

    def test(self, testing: TestingList) -> int:
        classifier = self.classifier
        test_results = (
            ClassifiedKnownSample(
                t.sample,
                classifier(
                    self.k, self.distance_function, self.training_data, t.sample
                ),
            )
            for t in testing
        )   
        pass_fail = map(
            lambda t: (1 if t.sample.species == t.classification else 0), test_results
        )
        return sum(pass_fail)


class Measured(NamedTuple):
    distance: float
    sample: TrainingKnownSample


def k_nn_1(
        k: int, dist: DistanceFunc, training_data: TrainingList, unknown: AnySample
) -> str:
    distances = sorted(map(lambda t: Measured(dist(t, unknown), t), training_data))
    k_nearest = distances[:k]
    k_frequencies: Counter[str] = collections.Counter(
        s.sample.sample.species for s in k_nearest
)
    mode, fq = k_frequencies.most_common(1)[0]
    return mode


def k_nn_b(
    k: int, dist: DistanceFunc, training_data: TrainingList, unknown: AnySample
) -> str:
    k_nearest = [
        Measured(float("inf"), cast(TrainingKnownSample, None)) for _ in range(k)
    ]
    for t in training_data:
        t_dist = dist(t, unknown)
        if t_dist > k_nearest[-1].distance:
            continue
        new = Measured(t_dist, t)
        k_nearest.insert(bisect.bisect_left(k_nearest, new), new)
        k_nearest.pop(-1)
    k_frequencies: Counter[str] = collections.Counter(
        s.sample.sample.species for s in k_nearest
    )
    mode, fq = k_frequencies.most_common(1)[0]
    return mode


def k_nn_q(
    k: int, dist: DistanceFunc, training_data: TrainingList, unknown: AnySample
) -> str:
    measured_iter = (Measured(dist(t, unknown), t) for t in training_data)
    k_nearest = heapq.nsmallest(k, measured_iter)
    k_frequencies: Counter[str] = collections.Counter(
        s.sample.sample.species for s in k_nearest
    )
    mode, fq = k_frequencies.most_common(1)[0]
    return mode


def test_classifier(
        training_data: list[TrainingKnownSample],
        testing_data: list[TestingKnownSample],
        classifier: Classifier) -> None:
    h = Hyperparameter(
        k=5,
        distance_function=manhattan,
        training_data=training_data,
        classifier=classifier)
    start = time.perf_counter()
    q = h.test(testing_data)
    end = time.perf_counter()
    print(
        f'| {classifier.__name__:10s} '
        f'| q={q:5}/{len(testing_data):5} '
        f'| {end-start:6.3f}s |')
                              
