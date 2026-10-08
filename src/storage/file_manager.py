from __future__ import annotations  # 1. 🌟 MUST BE LINE 1 (Tells Python to treat type annotations as string literals)

import json
import os
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING  # 2. Add this import

from services.exceptions import DatabaseError

if TYPE_CHECKING:
    from services.models.financetracker import BankData

# Dynamic file positioning relative to user home or project directory
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
FILE_PATH = DATA_DIR / "ledger.json"

def initialize_storage():
    """Ensures data directory and initial blank schema exists."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not FILE_PATH.exists():
        # This annotation is now safe at runtime!
        default_state: BankData = {
            "accounts": {}, 
            "transactions": [],
            "account_names": {}
        }
        with open(FILE_PATH, 'w') as f:
            json.dump(default_state, f, indent=4)

def load_data() -> "BankData":
    """Reads the JSON file and returns a structured dictionary."""
    initialize_storage()
    try:
        with open(FILE_PATH, 'r') as f:
            raw_data = json.load(f)
            
        # Pipeline Conversion: Convert string representations back to Datetime
        for acc_id, acc in raw_data.get("accounts", {}).items():
            acc["created_at"] = datetime.fromisoformat(acc["created_at"])
            
        for tx in raw_data.get("transactions", []):
            tx["timestamp"] = datetime.fromisoformat(tx["timestamp"])

        return raw_data
    
    except (json.JSONDecodeError, KeyError) as e:
        # Graceful fallback or error notification system if file gets physically modified maliciously
        print(f"❌ Storage Error: System file layout corrupt. Details: {e}")
        return {
            "accounts": {}, 
            "transactions": [],
            "account_names": {}
        }

def save_data(data: BankData) -> bool:
    """Safely records state updates using an atomic write pattern."""
    initialize_storage()
    tmp_file_path = FILE_PATH.with_suffix('.json.tmp')
    
    try:
        # Deep copy/prep dictionary for serialization
        serialized_data: BankData = {
            "accounts": {}, 
            "transactions": [],
            "account_names": {}
        }
        
        for acc_id, acc in data.get("accounts", {}).items():
            serialized_data["accounts"][acc_id] = {
                **acc,
                "created_at": acc["created_at"].isoformat() if isinstance(acc["created_at"], datetime) else acc["created_at"]
            }
            
        for tx in data.get("transactions", []):
            serialized_data["transactions"].append({
                **tx,
                "timestamp": tx["timestamp"].isoformat() if isinstance(tx["timestamp"], datetime) else tx["timestamp"]
            })

        # Step 1: Write to temporary file
        with open(tmp_file_path, 'w') as f:
            json.dump(serialized_data, f, indent=4)
            
        # Step 2: Atomic Swap (instantly overwrites old file, zero chance of halfway corrupt file)
        os.replace(tmp_file_path, FILE_PATH)
        return True
        
    except DatabaseError as e:
        if tmp_file_path.exists():
            os.remove(tmp_file_path)
        print(f"❌ Hardware IO Write Failure: {e}")
        return False
