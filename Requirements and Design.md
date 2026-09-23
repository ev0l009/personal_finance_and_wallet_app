# PERSONAL FINANCE & WALLET MANAGER

## 1. Requirements Interpretation

*   **Multi-Account Ledger:** The system must centralize management for various financial mediums (e.g., cash, banks, wallets), treating each account as an independent sub-ledger.

*   **Atomic Mutations:** Income, expenses, and transfers must immediately trigger accurate mathematical changes to affected accounts, maintaining a transparent audit trail.

*   **Dynamic Ledger Queries:** The historical logs must serve as a single source of truth, structured to support transaction tracking, multi-layered filtering, real-time balance calculations, provide useful transaction details and concise overviews of overall financial state without mathematical discrepancies.


## 2. Assumptions

*   **Account Deactivation where appropriate:** Accounts can be deactivated or permanently hard-deleted from the database. In order to protect historical financial context and overall net worth calculations accounts will be tagged either `Active`, `Deactivated` or `Missing/Deleted` in transaction history.

*   **Local Single-User Context:** The CLI application runs entirely within a local terminal environment. It assumes a single-user execution scope where authentication and network synchronization are not required.

* **Account Balance Limits:** The application shall also implement a reasonable limit on the number of accounts a user can have to prevent a possibly bloated database.

* **Account Balance & Transaction Limits:** At the CLI phase, the accounts will have a globally set maximum account balance. Relevant limits may also be placed on transaction amounts. This is to prevent bloated and overly-unrealistic transaction inputs.


## 3. Identified Ambiguities and resolution

- **Deactivate only empty accounts**  
    *Resolution:* An **empty account** is defined as a structural state where an account holds a balance absolutely equivalent to 0 or nil, i.e the account has no cash in it. 

- **Useful and concise overview of financial state**  
    *Resolution:* This is interpreted to be a time-bound calculation displaying **Total Income**, **Total Expenses**, and **Net Savings Rate** for the current calendar month.


## 4. Business Rules

### Account Management Rules

*   **Name Uniqueness:** Every account name must be unique (case-insensitive) to prevent user confusion during transfers.

*   **String Length Constraints:** Account names must be between 4 and 20 characters long and cannot consist purely of whitespace.

*   **Initialization Boundary:** A new account defaults to an empty starting balance equivalent to 0 unless a custom, positive opening balance is explicitly declared.

*   **Zero-Balance Deactivation:** An account can only be deactivated if its balance is exactly 0.00. If funds exist, the user must manually transfer them out first.

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
│   ├── __init__.py
│   ├── main.py              # App entry point; hosts the main menu loop
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── menus.py         # Sub-menus (Accounts menu, Transaction log display)
│   │   └── validators.py    # Console string-to-number check utilities
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ledger_service.py# Implements transfer, deposit, and validation math
│   │   ├── models.py        # Python dataclass objects (Account, Transaction)
│   │   └── exceptions.py    # Custom domain exceptions (e.g., InsufficientFundsError)
│   │
│   └── storage/
│       ├── __init__.py
│       └── file_manager.py  # Atomic JSON engine (safely handles load and save)
│
└── tests/
    ├── __init__.py
    └── test_ledger.py       # Pytest suite validating business logic blocks
```


## Data Model Proposal

The application will maintain its state inside a single localized document. We represent this via a JSON structure, paired with matching Python code representations (src/services/models.py) to enforce strong data typing.Proposed Storage Payload Blueprint (JSON Schema)Your JSON schema effectively links separate transaction operations back to their target account entities without duplicating raw state data.

```json
{
    "accounts": {
        "acc_01J8Y": {
            "id": "acc_01J8Y",
            "name": "Main Bank",
            "account_type": "bank",
            "balance": "1250.50",
            "is_active": true,
            "created_at": "2026-09-23T10:00:00Z"
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
```

### Logical Data Definitions (Python Implementation Mapping)
To manipulate this JSON structure safely, the backend service layer translates these elements into native `dataclass` objects. Crucially, all financial values are mapped to `Decimal` types rather than `float` to avoid terminal rounding errors:

- **Account Entity:** Tracks structural identity metadata (`id`, `name`, `account_type`), financial state (`balance`), and operational availability flags (`is_active`).

- **Transaction Entity:** Unifies deposits, withdrawals, and transfers under one unified schema. For standard single-account transactions (like deposits or withdrawals), the unneeded relational ID slot is assigned a value of None.


## Persistence Decision
We have selected local JSON file storage (data/ledger.json) as our persistence layer. It provides an optimal balance between simplicity and transparency for a standalone CLI tool.

To mitigate the inherent stability risks of flat-file storage, we enforce two engineering constraints:

### 1. The Atomic File Swap Engine (Anti-Corruption Pattern)

**The Risk:**  

- If a user closes their terminal shell or the computer suddenly crashes while the program is actively overwriting ledger.json, the file will break halfway, resulting in unreadable data loss.

**The Mitigating Strategy:** The system executes an Atomic Write-Ahead Replace workflow using Python's native os.replace() function:

- The updated data object is completely serialized and written out to a separate, temporary path (data/ledger.json.tmp).

- Once Python confirms the temporary file write has finished successfully, the operating system executes a low-level pointer shift, instantly renaming the .tmp file over the production ledger.json file. This guarantees that a partial file write can never occur.


### 2. High-Precision Data Serialization Pipeline

**The Constraint:** JSON cannot natively interpret complex Python data objects like decimal.Decimal or datetime.datetime.

**The Solution:** The storage/file_manager.py component implements a bilateral serialization conversion pipeline:

- **During Data Loading:** Strings representing numeric values (e.g., `"1250.50"`) and strings representing timestamps (e.g., `"2026-09-23T10:00:00Z"`) are parsed using Decimal() and datetime.fromisoformat() to prepare them for math logic operations.During 

- **Data Saving:** The structural objects are broken down back into base strings, ready to be dumped to flat JSON text lines.


## Error-Handling Strategy
To ensure a resilient user experience, the system enforces a strict "Catch and Recover" boundary pattern. The application isolates exceptions into three distinct technical layers, preventing hard crashes and code tracebacks from showing up in the user's terminal:

### 1. UI / Validation Failures (The Gatekeeper Layer)

- **When it triggers:** At the interactive command prompt, immediately upon reading keyboard input via input().

- **Scenarios handled:**: A user inputs non-numeric characters (e.g., "abc") into an amount field, or types a menu number choice that does not exist on the current screen.

- **Resolution action:**: The interface layer intercepts native Python exceptions like `ValueError`, completely halts downstream processing, prints a clear warning banner (e.g., ⚠️ Validation Error: Please enter a valid numeric amount), and smoothly re-renders the input loop.

### 2. Domain / Business Rule Violations (The Logic Layer)

- **When it triggers:** On application launch or during file-save sequences inside src/storage/file_manager.py.

- **Scenarios handled:**: The local ledger.json file is physically altered outside the application, causing corrupt text formatting or syntax issues.

- **Resolution action:**: The storage engine catches json.JSONDecodeError. Instead of crashing the whole executable, it initializes a clean, empty data structure ({"accounts": {}, "transactions": []}) to serve as a safety baseline and prints a diagnostic warning alert to the terminal screen.


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

- **Execution:** Tests verify that when a data dictionary is written to a temporary test file, decimal.Decimal components are safely written out as flat strings, and that they read back into memory correctly with matching precision values.

### UI / Smoke Testing Tier (Terminal Simulation)
- **Scope:** Simulates realistic user exploration sequences through the interactive prompts.

- **Execution:** We use pytest’s native monkeypatch utility to override the standard builtins.input mechanism. This feeds sequential arrays of text lines (e.g., ["1", "acc_main", "acc_savings", "100.00"]) into the run loop, verifying that screens transition cleanly from option to option without hanging.


## Explicit Out-of-Scope Decisions

To protect the delivery timeline and maintain a highly optimized, lightweight terminal tool, the following capabilities are explicitly classified as out-of-scope for this version of the application:

- **Multi-User Context & Session Access Control:** The application operates as a single-user ledger. It features no login passwords or permission levels. Data safety is assumed to be managed entirely via local operating system file permissions.

- **Multi-Currency Exchanges & Foreign Conversion Engine:** All fields process uniform, static currency values. There are no integrations with live exchange rate APIs.

- **Real-Time Network Persistence (Cloud Storage):** Data storage is completely isolated to a single, local file (data/ledger.json). External database connections (SQL Servers) or web API sync points are excluded.

- **Rich Graphical Visualization (GUI Engines):** Financial summaries will render using text layouts or structured ASCII tables directly inside standard terminal output lines (stdout). Generating visual window windows, charts, or images is out of scope.

- **Future-dated transactions**: This will not be implemented because this is primarily an offline CLI-based project and as such transactions cannot be scheduled at a future date.