from enum import Enum

from utils.validators import check_account_name
from utils.validators import require_no_null_negative_amount

from utils.helpers import generate_prefixed_id

import datetime

from typing import Self

from services.exceptions import InsufficientFundsError


from services.models.transaction import Withdrawal
from services.models.transaction import Deposit
from services.models.transaction import Transfer

from services import context

class AccountStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    # ARCHIVED = "archived"
 
class AccountType(Enum):
    BANK = "bank"
    SAVINGS = "savings"
    CASH = "cash"
    MOBILE = "mobile"

class Account:
    def __init__(
        self, 
        name: str, 
        account_type: str,
        balance: int = 0, 
    ):
        check_account_name(name, "Account Name") 

        self.id = generate_prefixed_id("acc")
        self.name = name
        self.account_type = account_type
        self.balance = balance
        self.account_status = AccountStatus.ACTIVE.value
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    def to_dict(self):
        """Converts the Account instance into a serializable dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "account_type": self.account_type,
            "balance": self.balance,
            "account_status": self.account_status,
            "created_at": self.created_at
        }

    def __str__(self) -> str:
        return (
            "==========================\n"
            f"    ACCOUNT INFO:\n"
            "==========================\n"
            f"Account ID: {self.id}\n"
            f"Account name: {self.name}\n"
            f"Creation date: {self.created_at}\n"
            f"Account Balance: {self.balance}\n"
            f"Account type: {self.account_type.capitalize()}\n"
            f"Account status: {self.account_status.capitalize()}\n"
        )
    
    def deactivate(self) -> Self:
        self.account_status = AccountStatus.INACTIVE.value
        return self

    def withdraw(self, amount: int, category: str) -> Self:
        require_no_null_negative_amount(amount)
        if amount > self.balance:
            raise InsufficientFundsError("Err: Account balance is lower than transaction amount")
        self.balance -= amount
        transaction = Withdrawal(amount, category)
        transaction.log_transaction()
        return self
    
    def deposit(self, amount: int) -> Self:
        require_no_null_negative_amount(amount)
        self.balance += amount
        transaction = Deposit(amount)
        transaction.log_transaction()
        return self
    
    def transfer(
        self, 
        recipient_acc: str, 
        amount: int
    ) -> Self:
        check_account_name(recipient_acc, "Account Name")
        
        # 3. Ensure the tracker is registered and grab it dynamically
        if context.active_tracker is None:
            raise RuntimeError("Application Error: Active Finance Tracker context not found.")
            
        recipient_id = context.active_tracker.get_account_id(recipient_acc)
        
        require_no_null_negative_amount(amount)
        if amount > self.balance:
            raise InsufficientFundsError("Err: Account balance is lower than transaction amount")
            
        transaction = Transfer(amount, self.id, recipient_id)
        transaction.log_transaction()
        return self