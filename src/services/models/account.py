from enum import Enum

from utils.validators import check_account_name
from utils.validators import require_no_null_negative_amount
from utils.helpers import generate_prefixed_id

import datetime

from typing import Self

from services.exceptions import InsufficientFundsError

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

    def withdraw(self, amount: int) -> Self:
        require_no_null_negative_amount(amount)
        if amount > self.balance:
            raise InsufficientFundsError("Err: Account balance is lower than transaction amount")
        self.balance -= amount
        return self
    
    def deposit(self, amount: int) -> Self:
        require_no_null_negative_amount(amount)
        self.balance += amount
        return self
    
    # def transfer