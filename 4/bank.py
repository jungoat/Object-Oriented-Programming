from decimal import Decimal
class InvalidWithdrawal(ValueError):
    def __init__(self, balance: Decimal, amount: Decimal) -> None:
        super().__init__(f"account doesn`t have ${amount}")
        self.amount = amount
        self.balance = balance
    def overage(self) -> Decimal:
        return self.amount - self.balance
    
try:
    balance = Decimal('25.00')
    raise InvalidWithdrawal(balance, Decimal('50.00'))
except InvalidWithdrawal as ex:
    print("I`m sorry, but your withdrawal is"
          "more than your balance by"
          f"${ex.overage()}")