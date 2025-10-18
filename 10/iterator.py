from typing import Iterable, Iterator


class CapitalIterable(Iterable[str]):
    def __init__(self, string: str) -> None:
        self.string = string

    def __iter__(self) -> Iterator[str]:
        return CapitalIterator(self.string)


class CapitalIterator(Iterator[str]):
    def __init__(self, string: str) -> None:
        self.words = [w.capitalize() for w in string.split()]
        self.index = 0

    def __next__(self) -> str:
        if self.index == len(self.words):
            raise StopIteration()
        
        word = self.words[self.index]
        self.index += 1
        return word
    
input_strings = ["1", "5", "28", "131", "3"]

output_integers = []
for num in input_strings:
    output_integers.append(int(num))

# 리스트 컴프리헨션
output_integers = [int(num) for num in input_strings]
output_integers = [int(num) for num in input_strings if len(num) < 3]
output_integers


from pathlib import Path
source_path = Path('src') / 'iterator_protocol.py'
with source_path.open() as source:
    examples = [line.rstrip() for line in source if ">>>" in line]

fantasy_authors = {b.author for b in books if b.genre == "fantasy"}

fantasy_titles = {b.title: b for b in books if b.genre == "fantasy"}

# 제너레이터 표현식
from pathlib import Path

full_log_path = Path.cwd() / "data" / "sample.log"
warning_log_path = Path.cwd() / "data" / "warnings.log"

with full_log_path.open() as source:
    warning_lines = (line for line in source if "WARN" in line)
    with warning_log_path.open("w") as target:
        for line in warning_lines:
            target.write(line)

            