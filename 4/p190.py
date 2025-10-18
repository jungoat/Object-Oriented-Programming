def divide_with_exception(dividend: int, divisor: int) -> None:
    try:
        print(f"{dividend/divisor=}")
    except ZeroDivisionError:
        print("You can`t divide by zero")

def divide_with_if(dividend: int, divisor: int) -> None:
    if divisor == 0:
        print("You can`t divide by zero")
    else:
        print(f"{dividend/ divisor=}")

class ItemType:
    def __init__(self, name: str) -> None:
        self.name = name
        self.on_hand = 0

class OutOfStock(Exception):
    pass

class InvalidItemType(Exception):
    pass

class Inventory:
    def __init__(self, stock: list[ItemType]) -> None:
        pass

    def lock(self, item_type: ItemType) -> None:
        pass

    def unlock(self, item_type: ItemType) -> None:
        pass

    def purchase(self, item_type: ItemType) -> int:
        if item_type.name == "Widget":
            raise OutOfStock(item_type)
        elif item_type.name == "Gadget":
            return 42
        else:
            raise InvalidItemType(item_type)
        
        