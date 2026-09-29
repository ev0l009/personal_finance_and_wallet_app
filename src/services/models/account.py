from enum import Enum

from utils.validators import check_account_name

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
        balance: int = 0, 
        account_type: str
    ):

        check_account_name(name)
        

        self.id = generate_prefixed_id("acc")
        self.name = name
        self.account_type = account_type
        self.balance = balance
        self.account_status = AccountStatus.ACTIVE.value
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")