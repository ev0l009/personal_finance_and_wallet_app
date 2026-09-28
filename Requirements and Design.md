# PERSONAL FINANCE & WALLET MANAGER

## 1. Requirements Interpretation

*   **Multi-Account Ledger:** The system must centralize management for various financial accounts (e.g., cash, banks, wallets), treating each account as an independent sub-ledger. It must handle account creation, provide lists of available accounts, give access to specific account and handle account deactivation or deletion.

*   **Atomic Mutations:** Income, expenses, and transfers must immediately trigger accurate mathematical changes to affected accounts, maintaining a transparent audit trail. Transfers by same user from one account to another account of theirs shouldn't within the application shouldn't affect net balance.

*   **Dynamic Ledger Queries:** The historical logs must serve as a single source of truth, structured to support transaction tracking, multi-layered search and filtering, provide useful transaction details and concise overviews of overall financial state without mathematical discrepancies.

*   **Persistent Data Storage:** The application must ensure the persistence of its data, so users should continue their sessions anytime even after exit.

*   **Intuitive CLI Interface:** The application's user interface should be intuitive and easy to use.

*   **Effective Error Handling & Robust Testing:** The application must be able to handle all relevant errors without affecting program flow and have a robust testing suite with adequate coverage of success paths, errors and edge cases.

*   **Detailed and Concise Documentation:** The application's documentation must provide essential information that helps user and developer quickly get used to the application.

## 2. Assumptions

*   **Permanent Data Retention:** Accounts cannot be permanently hard-deleted from the database. They can only change states (Active to Inactive) to protect historical financial context and overall net worth calculations.

*   **Local Single-User Context:** The CLI application runs entirely within a local terminal environment. It assumes a single-user execution scope where authentication and network synchronization are not required.


## 3. Identified Ambiguities and resolution

- **Deactivate only empty accounts**  
    *Resolution:* An **empty account** is defined as a structural state where an account holds a balance absolutely equivalent to 0 or nil, i.e the account has no cash in it. 

- **Useful and concise overview of financial state**  
    *Resolution:*
    ### Feature: Financial Overview & Audit Reporting

    **Core Objective**

    Provide users with a concise, time-bound overview of their financial health, detailing total income, total expenses, spending categories, and detailed account activity.

    **Income & Expense Logic**

    * **Inclusions:** Only deposits and withdrawals directly impact net balance calculations and are included in **Total Income** and **Total Expenses**.
    * **Exclusions:** Internal transfer transactions are excluded from net income and expense calculations to prevent double-counting.

    **Transfer Transaction Rules**

    * **Account Tagging:** To ensure clear distinction from deposits or withdrawals, both source and destination accounts tied to a transfer are tagged as `transfer`.
    * **Audit Trail:** Even though transfers do not alter aggregate net balance, they are fully recorded under **Account Activity** to maintain an accurate audit history.

    **Report Generation Filters**
    Reports use flexible filtering criteria to organize data, including:

    * **Timeframes:** Dynamic ranges (e.g., *This Week*, *Last 7 Days*, *Last Month*).
    * **Transaction Types:** *Deposits*, *Expenses*, or *Transfers*.
    * **Categories:** Specific expense types.


## 4. Business Rules

### Account Management Rules

*   **Name Uniqueness:** Every account name must be unique (case-insensitive) to prevent user confusion during transfers.

*   **String Length Constraints:** Account names must be between 4 and 20 characters long and cannot consist purely of whitespace.

*   **Initialization Boundary:** A new account defaults to an empty starting balance equivalent to 0 unless a custom, positive opening balance is explicitly declared.

*   **Zero-Balance Deactivation:** An account can only be deactivated if is empty. If funds exist, the user must manually transfer them out first.

*   **Visibility Filter:** Inactive accounts are excluded from everyday transaction choice menus but remain retrievable through an archival management menu.

### Transaction & Balance Rules

*   **Overdraft Protection:** A withdrawal transaction must be blocked with an error if the amount exceeds the account's available balance. Negative balances are prohibited.

*   **Self-Transfer Prevention:** The system must reject transactions where the source account ID matches the destination account ID.

*   **Immutability Flag:** Once a transaction is saved to the log, it cannot be edited or modified. To reverse a mistake, a counter-balancing transaction must be entered.


## Architecture Proposal

A Three-Tier Local Architecture optimized for an interactive CLI environment. By decoupling user prompts from core database states, we ensure that changes to the menu layout do not accidentally break financial math.

```text
 Interactive Text Menus  <--- (Runs the continuous 'while True' console loop)
            │
            ▼
 1. Command Parser     <--- Validates user menu inputs, numbers, and dates
            │
            ▼
 2. Service Layer      <--- Executes ledger math, transfers, & business rules
            │
            ▼
 3. Persistence Layer  <--- Handles atomic reads & writes to the local JSON file
```

### Architectural Component Responsibilities

- **The Interface Tier (Parser/UI):** Handles all terminal interactions (print and input). It captures user commands, ensures text fields are populated, and displays formatted tabular summaries back to the console.

- **The Logic Tier (Service):** The pure engine of the app. It manages incoming transaction logic, processes balance additions or deductions, evaluates custom business rule violations, and raises descriptive exceptions.

- **The Storage Tier (Persistence):** Manages file I/O operations. It parses data back and forth between raw JSON text and strongly typed Python memory data blocks.

## Proposed Project Structure

This directory blueprint mirrors our three-tier architecture proposal. It serves as a working baseline layout and will adapt organically during the coding phase:

```text
finance_ledger/
│
├── data/
│   └── ledger.json          # The localized JSON document storage file
│
├── src/
│   ├── main.py              # App entry point; hosts the main menu loop
│   │
│   ├── ui/
│   │   ├── menus.py         # Sub-menus (Accounts menu, Transaction log display)
│   │   └── validators.py    # Console string-to-number check utilities
│   │
│   ├── services/
│   │   ├── ledger_service.py# Implements transfer, deposit, and validation math
│   │   ├── models.py        # Python dataclass objects (Account, Transaction)
│   │   └── exceptions.py    # Custom domain exceptions (e.g., InsufficientFundsError)
│   │
│   └── storage/
│       └── file_manager.py  # Atomic JSON engine (safely handles load and save)
│
└── tests/
    └── test_ledger.py       # Pytest suite validating business logic blocks
```


## Data Model Proposal

The application will maintain its state inside a single localized document. This is presented in a JSON structure, paired with matching Python code representations (src/services/models.py) to enforce strong data typing.

### Proposed Storage Payload Blueprint (JSON Schema)
The JSON schema effectively links separate transaction operations back to their target account entities without duplicating raw state data:

```json
{
    "accounts": {
        "acc_01J8Y": {
            "id": "acc_01J8Y",
            "name": "Main Bank",
            "account_type": "bank",
            "balance": 125050,
            "is_active": true,
            "created_at": "2026-09-23T10:00:00Z"
        }
    },
    "transactions": [
        {
            "id": "tx_99A1Z",
            "transaction_type": "transfer",
            "amount": 15000,
            "source_account_id": "acc_01J8Y",
            "destination_account_id": "acc_02K9X",
            "category": "savings_allocation",
            "description": "Monthly savings transfer",
            "timestamp": "2026-09-23T11:30:00Z"
        },
        {
            "id": "tx_99A1Z",
            "transaction_type": "deposit",
            "amount": 10000,
            "source_account_id": "acc_01J8Y",
            "destination_account_id": "tx_99A1Z",
            "category": "savings_allocation",
            "description": "Monthly savings transfer",
            "timestamp": "2026-09-23T11:30:00Z"
        }
    ]
}
```

### Logical Data Definitions (Python Implementation Mapping)

To manipulate this JSON structure safely, the backend service layer translates these elements into native `dataclass` objects. Crucially, the Minor Units (Integer) Pattern will be employed and so all financial values are mapped to `int` types rather than `float` to avoid terminal rounding errors:

- **Account Entity:** Tracks structural identity metadata (`id`, `name`, `account_type`), financial state (`balance`), and operational availability flags (`is_active`).

- **Transaction Entity:** Unifies deposits, withdrawals, and transfers under one unified schema. For standard single-account transactions (like deposits or withdrawals), the unneeded relational ID slot is assigned a value of None while for transfer transactions involving more than one account, the IDs of both sender and receiver must be provided.


## Persistence Decision
A local JSON file storage (data/ledger.json) shall act as our persistence layer. It provides an optimal balance between simplicity and transparency for a standalone CLI tool.

To mitigate the inherent stability risks of flat-file storage, we enforce two engineering constraints:

### 1. The Atomic File Swap Engine (Anti-Corruption Pattern)

**The Risk:**  

- If a user closes their terminal shell or the computer suddenly crashes while the program is actively overwriting ledger.json, the file will break halfway, resulting in unreadable data loss.

**The Mitigating Strategy:** The system executes an Atomic Write-Ahead Replace workflow using Python's native os.replace() function:

- The updated data object is completely serialized and written out to a separate, temporary path (data/ledger.json.tmp).

- Once Python confirms the temporary file write has finished successfully, the operating system executes a low-level pointer shift, instantly renaming the .tmp file over the production ledger.json file. This guarantees that a partial file write can never occur.


### 2. High-Precision Data Serialization Pipeline

**The Constraint:** JSON cannot natively interpret complex Python data objects like datetime.datetime.

**The Solution:** The storage/file_manager.py component implements a bilateral serialization conversion pipeline:

- **During Data Loading:** Strings representing timestamps (e.g., `"2026-09-23T10:00:00Z"`) are parsed using datetime.fromisoformat() to prepare them for operations. 

- **During Data Saving:** The structural objects are broken down back into base strings, ready to be dumped to flat JSON text lines.


## Error-Handling Strategy
To ensure a resilient user experience, the system enforces a strict "Catch and Recover" boundary pattern. The application isolates exceptions into three distinct technical layers, preventing hard crashes and code tracebacks from showing up in the user's terminal:

### 1. UI / Validation Failures (The Gatekeeper Layer)

- **When it triggers:** At the interactive command prompt, immediately upon reading keyboard input via input().

- **Scenarios handled:**: A user inputs non-numeric characters (e.g., "abc") into an amount field, or types a menu number choice that does not exist on the current screen.

- **Resolution action:**: The interface layer intercepts native Python exceptions like `ValueError`, completely halts downstream processing, prints a clear warning banner (e.g., ⚠️ Validation Error: Please enter a valid numeric amount), and smoothly re-renders the input loop.

### 2. Domain / Business Rule Violations (The Logic Layer)

- **When it triggers:** Inside src/services/ledger_service.py after the input values have been confirmed as valid data types, but violate financial logical constraints.

- **Scenarios handled:**: Attempting to overspend an account's balance (insufficient funds), or attempting a transaction targeting a deactivated account.

- **Resolution action:**: The system raises custom, semantic exceptions (InsufficientFundsError, AccountInactiveError). The main interactive menu wrapper wraps service calls in a clean try-except block, catches these domain exceptions, and cleanly prints a transaction denial notice without risking local data corruption.

###  3. Storage Layer Failures (The Data Resiliency Layer)

- **When it triggers:** On application launch or during file-save sequences inside src/storage/file_manager.py.

- **Scenarios handled:** The local ledger.json file is physically altered outside the application, causing corrupt text formatting or syntax issues.

- **Resolution action:**: The storage engine catches json.JSONDecodeError. Instead of crashing the whole executable, it initializes a clean, empty data structure ({"accounts": {}, "transactions": []}) to serve as a safety baseline and prints a diagnostic warning alert to the terminal screen.

#### Possible exceptions list;

- InsufficientFundsError - Raised when an account balance falls below the transaction amount.

- NegativeAmountError - Raised when a negative value is provided for an amount field.

- InvalidFieldAttributeError - Raised when invalid/insufficient characters are used and the field in question is shown for context

- DuplicateAccountNameError - Raised when creating an account with same name as an already registered account

- InterAccountTransferMismatchError - Raised when a transfer debits the source account but fails to credit the destination account.

- DormantAccountError - Raised when attempting to log a transaction against an archive-only or closed financial account.

## Testing Strategy
An automated testing matrix using the pytest framework to systematically verify our business rules and boundaries before product deployment.

```text
 ┌──────────────────────┐
 │  1. Unit Tests       │ <--- Tests core calculations and custom domain errors
 └──────────────────────┘
            │
            ▼
 ┌──────────────────────┐
 │  2. Integration Tests│ <--- Tests the serialization conversion and file swapping
 └──────────────────────┘
            │
            ▼
 ┌──────────────────────┐
 │  3. UI / Smoke Tests │ <--- Simulates realistic keyboard choices via monkeypatching
 └──────────────────────┘
```

### 1. Unit Testing Tier (Isolated Logic)

- **Scope:** Focuses entirely on pure mathematical mutations and validation rules. It operates completely independent of files or terminal text.

- **Execution:** We use static mock dataset fixtures in memory. We explicitly pass test parameters to check things like:

* Ensuring a $50 deposit mathematically increments an account balance to exactly its expected target.

* Asserting that trying to trigger a transfer larger than an available balance correctly raises an `InsufficientFundsError`.

### 2. Integration Testing Tier (Storage Pipeline)

- **Scope:** Verifies that our serialization pipeline translates data types smoothly.

- **Execution:** Tests verify that when a data dictionary is written to a temporary test file, financial values are safely written out as integers, and that they read back into memory correctly with matching precision values.

### 3. UI / Smoke Testing Tier (Terminal Simulation)
- **Scope:** Simulates realistic user exploration sequences through the interactive prompts.

- **Execution:** We use pytest’s native monkeypatch utility to override the standard builtins.input mechanism. This feeds sequential arrays of text lines (e.g., `["1", "acc_main", "acc_savings", "100.00"]`) into the run loop, verifying that screens transition cleanly from option to option without hanging.


## Explicit Out-of-Scope Decisions

To protect the delivery timeline and maintain a highly optimized, lightweight terminal tool, the following capabilities are explicitly classified as out-of-scope for this version of the application:

- **Multi-User Context & Session Access Control:** The application operates as a single-user ledger. It features no login passwords or permission levels. Data safety is assumed to be managed entirely via local operating system file permissions.

- **Multi-Currency Exchanges & Foreign Conversion Engine:** All fields process uniform, static currency values. There are no integrations with live exchange rate APIs.

- **Real-Time Network Persistence (Cloud Storage):** Data storage is completely isolated to a single, local file (data/ledger.json). External database connections (SQL Servers) or web API sync points are excluded.

- **Rich Graphical Visualization (GUI Engines):** Financial summaries will render using text layouts or structured ASCII tables directly inside standard terminal output lines (stdout). Generating visual window windows, charts, or images is out of scope.


## NOTES

### Transaction schema shouldn't allow invalid states and should enforce immutablility

**Resolution:**

- Use

```python
@dataclass (frozen=True)
class Transaction:
    pass
```
to enforce immutability after validation and constructions (i.e. stops it from being changed after creation.).

*Note on Frozen Dataclasses:* If the dataclass is defined with `@dataclass(frozen=True)`, direct attribute assignment inside `__post_init__` will raise a `FrozenInstanceError`. You must use `object.__setattr__(self, 'field_name', value)` instead.

- Enforce validation before construction (i.e. stops it from being created wrong in the first place)

```python
@dataclass (frozen=True)
class Transaction:
    def __post_init__(self):
        pass
```


### Feature: Transaction Atomicity & Data Consistency

**Core Objective**

Ensure financial data integrity by making transfers fully atomic—guaranteeing that a transaction either executes completely across both accounts or leaves the database entirely untouched.

**Transfer Execution Workflow**

1. **Validation & Debit:** The app validates account details and debits the source account.
2. **Staging (In-Memory Storage):** Computed data for both sides of the transfer are stored in a temporary buffer before committing any primary database writes.
3. **Atomic Commit or Rollback:**
* **Success:** If no interruptions occur, all staged records are committed to the database simultaneously.
* **Failure/Interruption:** If an error occurs mid-process, the staged changes are discarded. No records are written to the database.


**Financial Audit Impact**

* **Zero Partial State:** A "half transfer" cannot exist in the application. Uncommitted transactions are completely erased from state.
* **Audit Integrity:** Only fully committed, two-sided transfers appear in **Account Activity** and reporting logs.