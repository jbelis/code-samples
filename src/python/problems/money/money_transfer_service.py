import logging
from decimal import Decimal
import sqlite3
from . import Account, Transaction, TransactionService

# Configure logging
logger = logging.getLogger(__name__)



class MoneyTransferService:

    def __init__(self):
        self.db = sqlite3.connect(":memory:")


    def transfer_funds(self, source: Account, target: Account, amount: Decimal, 
                      allow_duplicate_txn: bool = False) -> None:
        """
        Transfer funds between accounts with various validations.
        
        Args:
            source: Source account
            target: Target account
            amount: Amount to transfer
            allow_duplicate_txn: Whether to allow duplicate transactions
            
        Raises:
            ValueError: If source or target account is invalid
            RuntimeError: If insufficient balance or duplicate transaction
        """
        try:
            with self.db.cursor() as cursor:
                # Fetch source account
                cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (source.account_number,))
                result = cursor.fetchone()
                if not result:
                    raise ValueError("Invalid Source account number")
                
                source_account = Account(
                    account_number=result[0],  # Assuming column order matches Account fields
                    balance=result[1],
                    overdraft_allowed=result[2],
                    overdraft_limit=result[3]
                )

                # Fetch target account
                cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (target.account_number,))
                result = cursor.fetchone()
                if not result:
                    raise ValueError("Invalid Target account number")
                
                target_account = Account(
                    account_number=result[0],
                    balance=result[1],
                    overdraft_allowed=result[2],
                    overdraft_limit=result[3]
                )

                # Check balance and overdraft
                if not source_account.overdraft_allowed:
                    if (source_account.balance - amount) < 0:
                        raise RuntimeError("Insufficient Balance")
                else:
                    if ((source_account.balance + source_account.overdraft_limit) - amount) < 0:
                        raise RuntimeError("Insufficient Balance, Exceeding Overdraft Limit")

                # Check for duplicate transaction
                cursor.execute("""
                    SELECT target_account_number, amount 
                    FROM transactions 
                    WHERE source_account_number = %s 
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

                # Perform the transfer
                source_account.debit(amount)
                target_account.credit(amount)
                TransactionService.process_transaction(source_account, target_account, amount)
                
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
