from . import Account
from decimal import Decimal
import sqlite3
import logging

logger = logging.getLogger(__name__)

class AccountService:
    def __init__(self, transaction_service: TransactionService):
        self.db = sqlite3.connect(":memory:")
        self.transaction_service = transaction_service


    def getAccount(self, account_number: str) -> Account:
        with self.db.cursor() as cursor:
            # Fetch source account
            cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (account_number,))
            result = cursor.fetchone()
            if not result:
                return None
            
            return Account(
                account_number=result[0],  # Assuming column order matches Account fields
                balance=result[1],
                overdraft_allowed=result[2],
                overdraft_limit=result[3]
            )

    def transfer(self, source_account: Account, target_account: Account, amount: Decimal) -> None:
        try:

            with self.db.cursor() as cursor:
                source_account.debit(amount)
                target_account.credit(amount)
                self.transaction_service.process_transaction(source_account, target_account, amount)
                cursor.connection().commit()
        
        except Exception as e:
            if cursor:
                cursor.connection().rollback()
            logger.error("Error during fund transfer", exc_info=True)
            raise

        finally:
            try:
                if cursor:
                    cursor.connection.close()
            except Exception as e:
                logger.error("Error closing database connection", exc_info=True)

