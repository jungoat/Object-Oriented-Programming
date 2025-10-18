import math
'''
class Point:
    def __init__(self, x: float, y: float) -> None:
        self.move(x, y)
'''
class Point:
    def __init__(
            self,
            x: float = 0,
            y: float = 0
    ) -> None:
        self.move(x,y)

    def move(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def reset(self) -> None:
        self.move(0, 0)

    def caculate_distance(self, other: "Point") -> float:
        return math.hypot(self.x - other.x , self.y - other.y)
    
point = Point(3, 5)
print(point.x, point.y)