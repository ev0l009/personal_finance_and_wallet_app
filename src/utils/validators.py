import string

from services.exceptions import InvalidFieldAttributeError
from services.exceptions import InvalidAmountError

MIN_ACCOUNT_NAME_LENGTH = 4
MAX_ACCOUNT_NAME_LENGTH = 20

def check_account_name(name: str, field: str):
    if not name.strip():
        raise InvalidFieldAttributeError(f"Err: {field} cannot be an empty.")
    
    if len(name) < MIN_ACCOUNT_NAME_LENGTH or len(name) > MAX_ACCOUNT_NAME_LENGTH:
        raise InvalidFieldAttributeError(f"Err: {field} requires {MIN_ACCOUNT_NAME_LENGTH}-{MAX_ACCOUNT_NAME_LENGTH} characters")

    valid_character_pool = string.ascii_letters + string.digits

    for char in name.replace(" ", ""):
        if char not in valid_character_pool:
            raise InvalidFieldAttributeError(f"Err: {field} requires only alphabets and numbers.")
        

def require_no_null_negative_amount(amount: int):
    if amount <= 0:
        raise InvalidAmountError("Err: Amount must be greater than zero.")

def check_account_exists(account_name: str):
    