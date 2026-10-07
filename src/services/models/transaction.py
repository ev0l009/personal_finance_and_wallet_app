import datetime

from enum import Enum

from utils.helpers import generate_prefixed_id

from services import context

class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"

class Transaction:
    def __init__(
        self, 
        amount: int 
    ) -> None:
        self.id = generate_prefixed_id("trx")
        self.amount = amount
        self.transaction_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
 
    def log_transaction(self) -> None:
        #  Ensure the tracker has been initialized
        if context.active_tracker is None:
            raise RuntimeError("Context Error: Active Finance Tracker context not found.")
        
        #  Pull the database dict directly from your active context instance
        context.active_tracker.data["transactions"].append(self.__dict__)

class Deposit(Transaction):
    def __init__(self, amount: int) -> None:
        super().__init__(amount)
        self.transaction_type = TransactionType.DEPOSIT.value

class Withdrawal(Transaction):
    def __init__(
        self, 
        amount: int, 
        category: str
    ) -> None:
        super().__init__(amount)
        self.transaction_type = TransactionType.WITHDRAWAL.value
        self.category = category

class Transfer(Transaction):
    def __init__(
        self, 
        amount: int, 
        source_account_id: str, 
        destination_account_id: str
    ) -> None:
        super().__init__(amount)
        self.transaction_type = TransactionType.TRANSFER.value
        self.source_account_id = source_account_id
        self.destination_account_id = destination_account_id