from collections.abc import Container
Container.__abstractmethods__
frozenset({'__contains__'})

help(Container.__contains__)


from collections.abc import Container

class OddIntegers:
    def __contains__(self, x: int) -> bool:
        return x % 2 != 0
    
odd = OddIntegers
isinstance(odd, Container)
issubclass(OddIntegers, Container)

odd = OddIntegers()
1 in odd
2 in odd
3 in odd