class Database:
    """데이터베이스 클래스 구현"""

    def __init__(self, connection: Optional[str] = None) -> None:
        """데이터베이스에 대한 연결 생성"""
        pass

database = Database("path/to/data")

from ecommerce.database import database
from typing import Optional

db: Optional[Database] = None

def initialize_database(connection: Optional[str] = None) -> None:
    global db
    db = Database(connection)

def get_database(connection: Optional[str] = None) -> None:
    global db
    if not db:
        db = Database(connection)
    return db

class Point:
    """점을 2차원 좌표로 표현한다."""
    pass

def main() -> None:
    """
    유용한 작업을 수행한다.
    
    >>> main()
    p1.calculate_distance(p2)=5.0
    """
    p1 = Point()
    p2 = Point(3, 4)
    print(f"{p1.calculate_distance(p2)=}")

if __name__ =="__main__":
    main()