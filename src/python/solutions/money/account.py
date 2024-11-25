from decimal import Decimal
from dataclasses import dataclass

@dataclass
class Account:
    account_number: str
    balance: Decimal
    overdraft_allowed: bool = False
    overdraft_limit: Decimal = Decimal('0')

    def debit(self, amount: Decimal) -> None:
        self.balance -= amount

    def credit(self, amount: Decimal) -> None:
        self.balance += amount

    def hasSufficientBalance(self, amount: Decimal) -> bool:
        if not self.overdraft_allowed:
            if (self.balance - amount) < 0:
                return False
        else:
            if ((self.balance + self.overdraft_limit) - amount) < 0:
                return False

