import logging
from decimal import Decimal
import sqlite3
from . import Account, Transaction, TransactionService, AccountService

# Configure logging
logger = logging.getLogger(__name__)



class MoneyTransferService:

    def __init__(self, accountService: AccountService, transactionService: TransactionService):
        self.db = sqlite3.connect(":memory:")
        self.accountService = accountService
        self.transactionService = transactionService


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
        # Fetch source account
        source_account = self.accountService.getAccount(source.account_number)
        if not source_account:
            raise ValueError("Invalid Source account number")
        
        # Fetch target account
        target_account = self.accountService.getAccount(target.account_number)
        if not source_account:
            raise target_account("Invalid target account number")
        
        # Check balance and overdraft
        if not source_account.hasSufficientBalance(amount):
            raise RuntimeError("Insufficient Balance")
        
        # Check for duplicate transaction
        if not allow_duplicate_txn:
            existing_transactions = self.transactionService.find_transactions_for_account(source_account, target_account, amount)
            if existing_transactions:
                raise RuntimeError("Duplicate transaction exception")
        
        # Perform the transfer
        self.accountService.transfer(source_account, target_account, amount)

