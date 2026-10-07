class FinanceTrackerException(Exception):
    pass

class InvalidFieldAttributeError(FinanceTrackerException):
    pass

class DuplicateAccountNameError(FinanceTrackerException):
    pass

class TransactionException(FinanceTrackerException):
    pass

class InsufficientFundsError(TransactionException):
    pass

class InvalidAmountError(TransactionException):
    pass

class AccountNotFoundError(FinanceTrackerException):
    pass