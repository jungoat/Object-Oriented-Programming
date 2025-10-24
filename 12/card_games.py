from __future__ import annotations
import abc
import collections
import random
from enum import Enum, auto
from typing import (
    Any,
    Counter,
    Iterator,
    Iterable,
    List,
    NamedTuple,
    TypeVar,
    cast,
)


class Suit(str, Enum):
    Clubs = "\N{Black Club Suit}"
    Diamonds = "\N{Black Diamond Suit}"
    Hearts = "\N{Black Heart Suit}"
    Spades = "\N{Black Spade Suit}"


class Card(NamedTuple):
    """
    >>> c = Card(5, Suit.Spades)
    >>> print(c)
    5♠
    >>> c
    Card(rank=5, suit=<Suit.Sapdes: '♠'>)
    
    """

    rank: int
    suit: Suit

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"


class Trick(int, Enum):
    pass


class Hand(List[Card]):
    def __init__(self, *cards: Card) -> None:
        super().__init__(cards)

    def scoring(self) -> list[Trick]:
        pass


class CardGameFactory(abc.ABC):
    @abc.abstractmethod
    def make_card(self, rank: int, suit: Suit) -> "Card":
        ...

    @abc.abstractmethod
    def make_hand(self, *cards: Card) -> "Hand":
        ...


class CribbageCard(Card):
    @property
    def points(self) -> int:
        return self.rank
    

class CribbageAce(Card):
    @property
    def points(self) -> int:
        return 1
    

class CribbageFace(Card):
    @property
    def points(self) -> int:
        return 10
    

class CribbageTrick(Trick):
    Fifteen = auto()
    Pair = auto()
    Run_3 = auto()
    Run_4 = auto()
    Run_5 = auto()
    Right_Jack = auto()


import itertools

C = TypeVar("C")


def powerset(iterable: Iterable[C]) -> Iterable[tuple[C, ...]]:
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1)
    )


class CribbageHand(Hand):
    starter: Card

    def upcard(self, starter: Card) -> "Hand":
        self.starter = starter
        return self
    
    def scoring(self) -> list[Trick]:
        return tricks
    

class PokerCard(Card):
    def __str__(self) -> str:
        if self.rank == 14:
            return f"A{self.suit}"
        return f"{self.rank}{self.suit}"
    

class PokerHand(Hand):
    def scoring(self) -> list[Trick]:
        return [rank]
    

class PokerFactory(CardGameFactory):
    def make_card(self, rank: int, suit: Suit) -> "Card":
        if rank == 1:
            rank = 14
        return PokerCard(rank, suit)
    
    def make_hand(self, *cards: Card) -> "Hand":
        return PokerHand(*cards)