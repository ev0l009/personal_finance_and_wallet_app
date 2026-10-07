# from services.exceptions import InvalidFieldAttributeError
from services.exceptions import DuplicateAccountNameError
from services.exceptions import InsufficientFundsError
from services.exceptions import InvalidAmountError

from services import context

from services.models.financetracker import FinanceTracker
from services.models.account import Account
# from services.models.transaction import Transaction

from services.models.account import AccountType

bank_acc = Account("Bank Acc", AccountType.BANK.value)
cash_acc = Account("Cash Acc", AccountType.CASH.value)

# try:
#     my_acc = Account("My account", AccountType.CASH.value)
#     # my_acc.deactivate()
# except InvalidFieldAttributeError as err:
#     print(err)
# else:
#     print(my_acc)

# 1. Instantiate your single CLI tracker
finance_tracker = FinanceTracker()

# 2. Store it globally inside the context hub
context.active_tracker = finance_tracker

try:
    (
        finance_tracker
            .register_account(bank_acc)
            .register_account(cash_acc)
    )
except DuplicateAccountNameError as err:
    print(err)
else:
    print(finance_tracker.data["account_names"])

try:
    (
        bank_acc
            .deposit(10000)
            .withdraw(2000, "Test")
            .transfer("Cash Acc",5000)
    )
except InvalidAmountError as err:
    print(err)
except InsufficientFundsError as err:
    print(err)
else:
    print(finance_tracker.data["transactions"])