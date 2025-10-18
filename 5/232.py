from urllib.request import urlopen
from typing import Optional, cast, List

class WebPage:
    def __init__(self, url: str) -> None:
        self.url = url
        self._content: Optional[bytes] = None

    @property
    def content(self) -> None:
        if self._content is None:
            print("새 페이지 조회...")
            with urlopen(self.url) as response:
                self._content = response.read()
        return self._content
    
import time

webpage = WebPage("http://ccphillips.net/")

now = time.perf_counter()
content1 = webpage.content
first_fetch = time.perf_counter() - now

now = time.perf_counter()
content2 = webpage.content
second_fetch = time.perf_counter() - now

assert content2 == content1, "Problem: Pages were different"
print(f"Initial Request {first_fetch:.5f}")
print(f"Subsequent Requests {second_fetch:.5f}")

class AverageList(List[int]):
    @property
    def average(self) -> float:
        return sum(self) / len(self)
    
a = AverageList([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5])
print(a.average)