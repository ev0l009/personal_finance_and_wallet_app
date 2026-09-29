from enum import Enum

from utils.validators import check_account_name

from utils.helpers import generate_prefixed_id

import datetime

class AccountStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"

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
            f"Account type: {self.account_type.capitalize()}\n"
            f"Status: {self.account_status.capitalize()}\n"
        )