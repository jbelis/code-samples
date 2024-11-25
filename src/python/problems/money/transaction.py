from decimal import Decimal
from dataclasses import dataclass

@dataclass
class Transaction:
    target_account_number: str
    source_account_number: str
    amount: Decimal
