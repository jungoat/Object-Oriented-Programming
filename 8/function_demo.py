from __future__ import annotations
import heapq
import time
from typing import Any, Optional, cast, Callable
from dataclasses import dataclass, field

Callback = Callable[[int], None]

@dataclass(frozen=True, order=True)
class Task:
    scheduled: int
    callback: Callback = field(compare=False)
    delay: int = field(default=0, compare=False)
    limit: int = field(default=1, compare=False)

    def repeat(self, current_time: int) -> Optional["Task"]:
        if self.delay > 0 and self.limit > 2:
            return Task(
                current_time + self.delay,
                cast(Callback, self.callbck),
                self.delay,
                self.limit - 1,
            )
        elif self.delay >  0 and self.limit == 2:
            return Task(
                current_time + self.delay,
                cast(Callback, self.callback),
            )
        else:
            return None
        
class Scheduler:
    def __init__(self) -> None:
        self.tasks: list[Task] = []

    def enter(
            self,
            after: int,
            task: Callback,
            delay: int = 0,
            limit: int = 1,
    ) -> None:
        new_task = Task(after, task,delay, limit)
        heapq.heappush(self.tasks, new_task)

    def run(self) -> None:
        current_time = 0
        while self.tasks:
            next_task = heapq.heappop(self.tasks)
            if (delay := next_task.scheduled - current_time) > 0:
                time.sleep(next_task.scheduled - current_time)
            current_time = next_task.scheduled
            next_task.callback(current_time)
            if again := next_task.repeat(current_time):
                heapq.heappush(self.tasks, again)

    
import datetime


def format_time(message: str) -> None:
    now = datetime.datetime.now()
    print(f"{now:%I:%M:%S}: {message}")


def one(timer: float) -> None:
    format_time("Called One")


def two(timer: float) -> None:
    format_time("Called Two")


def three(timer: float) -> None:
    format_time("Called Three")


class Repeater:
    def __init__(self) -> None:
        self.count = 0

    def four(self, timer: float) -> None:
        self.count += 1
        format_time(f"Called Four: {self.count}")


class Repeater_2:
    def __init__(self) -> None:
        self.count = 0

    def __call__(self, timer: float) -> None:
        self.count += 1
        format_time(f"Called Four: {self.count}")



__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}

if __name__ == "__main__":
    s = Scheduler()
    s.enter(1, one)
    s.enter(2, one)
    s.enter(2, two)
    s.enter(4, two)
    s.enter(3, three)
    s.enter(6, three)
    repeater = Repeater()
    s.enter(5, repeater.four, delay=1, limit=5)
    s.run()

    s2 = Scheduler()
    s2.enter(5, Repeater_2(), delay=1, limit=5)
    s2.run()


class A:
    def show_something(self):
        print("My class is A")

a_object = A()
a_object.show_something()

def patched_show_something():
    print("My class is NOT A")
    

a_object.show_something = patched_show_something
a_object.show_something

b_object = A()
b_object.show_something()

class Repeater_2:
    def __init__(self) -> None:
        self.count = 0

    def __call__(self, timer: float) -> None:
        self.count += 1
        format_time(f"Called Four: {self.count}")

rpt = Repeater_2()

contents = "Some file contents\n"
file = open("filename.txt", "w")
file.write(contents)
file.close()

with open("big_nuimber.txt") as input:
    for line in input:
        print(line)


results =str(2**2048)
with open("big_number.txt", "w") as output:
    output.write("# A big number \n")
    output.writelines(
        [
            f"{len(results)}\n",
            f"{results}\n"
        ]
    )

from pathlib import Path


source_path = Path("requiremnets.txt")
with source_path.open() as source_file:
    for line in source_file:
        print(line, end='')


class StringJoiner(list):
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.result = "".join(self)


from typing import List, Optional, Type, Literal
from types import TracebackType

class StringJoiner(List[str]):
    def __enter__(self) -> "StringJoiner":
        return self
    
    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ) -> Literal[False]:
        self.result = "".join(self)
        return False

class StringJoiner2(List[str]):
    def __init__(self, *args: str) -> None:
        super().__init__(*args)
        self.result = "".join(self)


from contextlib import contextmanager
from typing import List, Any, Iterator

@contextmanager
def joiner(*args: Any) -> Iterator[StringJoiner2]:
    string_list = StringJoiner2(*args)
    try:
        yield string_list
    finally:
        string_list.result = "".join(string_list)
        