from decimal import Decimal
from . import Account

class TransactionService:
    def __init__(self):
        self.db = sqlite3.connect(":memory:")


    def process_transaction(self, source: Account, target: Account, amount: Decimal) -> None:
        pass


    def find_transactions_for_account(self, source_account: Account, target_account: Account, amount: Decimal) -> None:
        with self.db.cursor() as cursor:
                cursor.execute("""
                    SELECT target_account_number, amount 
                    FROM transactions 
                    WHERE source_account_number = %s and target_account_number = %s and amount = %s
                    ORDER BY transaction_date DESC 
                    LIMIT 1
                """, (source_account.account_number,))
                
                last_txn = cursor.fetchone()
                if last_txn:
                    last_transaction = Transaction(
                        target_account_number = last_txn[0],
                        amount=last_txn[1]
                    )
                    if (last_transaction.target_account_number == target_account.account_number and 
                        last_transaction.amount == amount and 
                        not allow_duplicate_txn):
                        raise RuntimeError("Duplicate transaction exception")
