from services.models.account import Account

from services.exceptions import DuplicateAccountNameError

from typing import Self
from typing import TypedDict


class TransactionInfo(TypedDict):
    id: str
    transaction_type: str
    amount: int
    timestamp: str

class BankData(TypedDict):
    accounts: dict[str, Account]
    transactions: list[TransactionInfo]
    account_names: dict[str, str]


class FinanceTracker:
    def __init__(self):
        self.data: BankData = {
            "accounts": {},
            "transactions": [],
            "account_names": {}
        }

    def register_account(self, account: "Account") -> Self:
        normalized_name = account.name.replace(" ", "").lower()
        
        if normalized_name in self.data["account_names"]:
            raise DuplicateAccountNameError("Account name already exists")
            
        self.data["accounts"][account.id] = account
        self.data["account_names"][normalized_name] = account.id
        
        return self
    
    def __str__(self) -> str:
        return (
            "-----------------------------------\n"
            "       Finance Tracker Logs        \n"
            "-----------------------------------\n"
            f"|  Number of accounts       |  {len(self.data['accounts'])}    \n"
            f"|  Number of transactions   |  {len(self.data['transactions'])}    \n"
        )
    
    def accounts_list(self) -> str:
        account_list: str = (
            "  S/N  |  Account Name  |  Account ID |  Balance  \n"
            "--------------------------------------------------\n"
        )
        for idx, account in enumerate(self.data["accounts"].values()):
            account_list += (
                f"  {idx+1}    |  {account.name}    |  {account.id}  |  {account.balance}  \n"
                "--------------------------------------------------\n"
            )
        return account_list

    # def log_transaction(self, transaction: "Transaction") -> Self:
    #     self.data["transactions"][transaction.id] = 
    #     return self