requirements interpretation
assumptions
identified ambiguities
business rules you've chosen
architecture proposal
project structure
data model
persistence decision
error-handling strategy
testing strategy
explicit out-of-scope decisions


# PERSONAL FINANCE & WALLET MANAGER

## Requirements Interpretation
### Accounts
**Goal**: A user must be able to create and manage multiple financial accounts from a central point.

**Assumption**: Accounts can be deactivated not deleted to preserve financial records.

**Architecture**: Every account will have attributes including name, balance, transaction history.

**Business rules**
- **Account Modification**
    * Every account name must be unique
    * Every account name must be at least 4 and 20 characters long
    * A new account's initial balance starts from 0.00 by default or a custom opening balance

- **Account Deactivation**
    * A user cannot deactivate a non-empty account 
    * All funds must be transfered an active account before deactivation.
    * Deactivated accounts will be hidden but can be retrieved and reactivated at any time


### Income & Expenses
**Goal**: Each account must track its own withdrawal, deposits, provide useful information about transaction and update its balance accordingly.

### Transfers
**Goal**: Users must be able to transfer money to their other activated accounts without without affecting overall balance across all accounts.


### Transaction history
**Goal**: Transaction history should provide useful information including;
    - transaction type (deposit,withdrawal,transfer)
    - transaction time
    - transaction amount
    - transaction account
    - optional categories (eg groceries, transport, airtime)
    - quick description information about the transaction


### Searching and filtering
**Goal**: Users can search and retrieve specific transaction details easily and quickly through flexible filters and recieve appropriate feedback


### Balances
**Goal**: Users can access their overall balance and individual balances across all their active accounts without discrepancies.


### Financial summaries
**Goals**: Users should have useful and concise overview of their financial state.



## Architecture Proposal
### CLI-based version
 Terminal / CLI Input  
            │
            V
 1. Command Parser     <--- Validates flags, arguments, & commands
            │
            V
 2. Service Layer      <--- Executes business rules & financial math
            │
            ▼
 3. Storage Layer      <--- Reads / writes to local JSON


## Data Model
{
    "accounts": {
        "acc_01J8Y": {
            "id": "acc_01J8Y",
            "name": "Main Bank",
            "account_type": "bank",
            "balance": "1250.50",
            "is_active": true,
            "created_at": "2026-09-23T10:00:00Z"
        },
        "acc_02K9X": {
            "id": "acc_02K9X",
            "name": "Savings",
            "account_type": "savings",
            "balance": "5000.00",
            "is_active": true,
            "created_at": "2026-09-23T10:15:00Z"
        }
    },
    "transactions": [
        {
            "id": "tx_99A1Z",
            "transaction_type": "transfer",
            "amount": "150.00",
            "source_account_id": "acc_01J8Y",
            "destination_account_id": "acc_02K9X",
            "category": "savings_allocation",
            "description": "Monthly savings transfer",
            "timestamp": "2026-09-23T11:30:00Z"
        }
    ]
}



## Persistence Decision
- Atomic Updates: The system will never write directly to the active storage ledger.json file. Instead, it writes to a temporary file (ledger.json.tmp) first. Once the write operation completes perfectly, it instantly swaps it with the real file using an OS-level atomic operation (os.replace).
- Data Conversion Pipeline: Since JSON cannot natively store Python Decimal data types or datetime timestamps. The data access code will act as a pipeline—converting raw strings back into high-precision types when loading, and serializing them down to strings when saving.


## Errors
Error concerns will be separated;
- **UI/Validation Errors**: Checked instantly at the terminal prompt (e.g., typing "abc" instead of a number, choosing option 7 when only options 1-4 exist). The system catches these before running any calculations.

- **Domain/Business Rule Errors:**: Raised by the logical engine when data looks valid, but rules are broken (e.g., trying to withdraw $100 when the account only has $50, or attempting to transfer to a deactivated account).

- **Storage Layer Errors**: Catches json.JSONDecodeError and provides user feedback.


## Testing
   1. Unit Tests        <--- Tests core math & business exceptions (No UI, No IO)
            │
            V
   2. Integration Tests <--- Tests that Service Layer safely reads/writes JSON
            │
            V
   3. UI / Smoke Tests  <--- Simulates keyboard inputs into the interactive menus
 
