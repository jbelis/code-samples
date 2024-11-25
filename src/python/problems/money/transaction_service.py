from decimal import Decimal
from . import Account

class TransactionService:
    @staticmethod
    def process_transaction(source: Account, target: Account, amount: Decimal) -> None:
        # Implementation for saving transaction
        pass
