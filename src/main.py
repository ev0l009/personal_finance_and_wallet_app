from services.exceptions import InvalidFieldAttributeError
from services.exceptions import DuplicateAccountNameError
from services.exceptions import InsufficientFundsError
from services.exceptions import InvalidAmountError

from services.models.account import Account

from services.models.account import AccountType

from services.models.financetracker import FinanceTracker

bank_acc = Account("Bank Acc", AccountType.BANK.value)
cash_acc = Account("Cash Acc", AccountType.CASH.value)
mobile_acc = Account("Mobile Acc", AccountType.MOBILE.value)
savings_acc = Account("Savings Acc", AccountType.SAVINGS.value)

try:
    my_acc = Account("My account", AccountType.CASH.value)
    # my_acc.deactivate()
except InvalidFieldAttributeError as err:
    print(err)
# else:
#     print(my_acc)

finance_tracker = FinanceTracker()

try:
    (
        bank_acc
            .deposit(10000)
            .withdraw(100000)
    )
except InvalidAmountError as err:
    print(err)
except InsufficientFundsError as err:
    print(err)
else:
    print(bank_acc)


try:
    (
        finance_tracker
            .register_account(bank_acc)
            .register_account(cash_acc)
            .register_account(mobile_acc)
            .register_account(savings_acc)
    )
except DuplicateAccountNameError as err:
    print(err)
# else:
#     print(finance_tracker.accounts_list())

