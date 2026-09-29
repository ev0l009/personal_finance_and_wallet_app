import string

from services.exceptions import InvalidFieldAttributeError

from services.models.account import Account

from services.models.account import AccountType


try:
    my_acc = Account("My account", AccountType.CASH.value)
except InvalidFieldAttributeError as err:
    print(err)
else:
    print(my_acc)