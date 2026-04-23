"""
Module to perform a full check of the SQLite integration in WPipe.

This script tests the creation of a database, writing and reading records,
and inspecting the results using both the WPipe SQLite wrapper and WSQLite.
"""

import os
import tempfile
from typing import List, Dict, Any

from wsqlite import WSQLite
from wpipe.sqlite import SQLite
from wpipe.sqlite.tables_dto.records import RecordModel

def run_performance_check() -> None:
    """
    Execute a performance and integration check on the SQLite database.
    """
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
        db_path: str = temp_file.name

    try:
        # Use standard WPipe SQLite wrapper
        db_instance: SQLite = SQLite(db_path)
        input_data: Dict[str, Any] = {"test": "performance"}
        rid: int = db_instance.write(input_data=input_data)
        print(f"Inserted ID: {rid}")

        record: Any = db_instance.read_by_id(rid)
        print(f"Read record: {record}")

        # Inspection using pure WSQLite (No sqlite3 import)
        inspector: WSQLite = WSQLite(RecordModel, db_path)
        all_rows: List[RecordModel] = inspector.get_all()
        print(f"Rows found via WSQLite: {len(all_rows)}")
        for row in all_rows:
            print(f" - Data: {row.input_data}")

    finally:
        if os.path.exists(db_path):
            os.remove(db_path)

if __name__ == "__main__":
    run_performance_check()
