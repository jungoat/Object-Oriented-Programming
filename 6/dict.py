d = {"a": 42, "a":3.14}
d
from __future__ import annotations
from typing import cast, Any, Union, Tuple, Dict, Iterable, Mapping
from collections import Hashable

DictInit = Union[Iterable[Tuple[Hashable, Any]], Mapping[Hashable, Any],None]

class NoDupDict(Dict[Hashable, Any]):
    def __setitem__(self, key: Hashable, value:Any) -> None:
        if key in self:
            raise ValueError(f"duplicate {key!r}")
        super().__setitem__(key, value)

    def __init__(self, init: DictInit = None, **kwargs: Any) -> None:
        if isinstance(init, Mapping):
            super().__init__(init, **kwargs)
        elif isinstance(init, Iterable):
            for k, v in cast(Iterable[Tuple[Hashable, Any]], init):
                self[k] = v
        elif init is None:
            super().__init__(**kwargs)
        else:
            super().__init__(init, **kwargs)


import logging
from functools import wraps
from typing import Type, Any


class DieMeta(abc.ABCMeta):
    def __new__(
        metaclass: Type[type],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **kwargs: Any,
    ) -> "DieMeta":
        if "roll" in namespace and not getattr(
            namespace["roll"], "__isabstractmethod__", False
        ):
            namespace.setdefault("logger", logging.getLogger(name))

            original_method = namespace["roll"]

            @wraps(original_method)
            def logged_roll(self: "DieLog") -> None:
                original_method(self)
                self.logger.info(f"Rolled {self.face}")

            namespace["roll"] = logged_roll
        new_object = cast(
            "DieMeta", abc.ABCMeta.__new__(metaclass, name, bases, namespace)
        )
        return new_object
    

class DieLog(metaclass=DieMeta):
    logger: logging.Logger

    def __init__(self) -> None:
        self.face: int
        self.roll()

    @abc.abstractmethod
    def roll(self) -> None:

    def __repr__(self) -> str:
        return f"{self.face}"
    

class D6L(DieLog):
    def roll(self) -> None:
        """Some documentation on D6L"""
        self.face = random.randrange(1, 7)



test_d6l = """
>>> random.seed($2)
>>> d = D6L()
>>> d.face
6

>>> import sys
>>> logging.basicConfig(stream=sys.stdout, level=logging.INFO)
>>> de = D6L()
INFO:D6L:Rolled 1
>>> d2.face
1
"""

__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
