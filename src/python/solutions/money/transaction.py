from decimal import Decimal
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    target_account_number: str
    source_account_number: str
    amount: Decimal
    transaction_date: datetime
