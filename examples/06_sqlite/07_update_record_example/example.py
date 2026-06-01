"""
05 SQLite - Update and Delete Records

Shows updating and deleting records in SQLite.
"""

import os

from wpipe.sqlite import Wsqlite, SQLite


def main() -> None:
    """Run update and delete example."""
    db_path: str = "test_update.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    with Wsqlite(db_path) as db:
        db.input = {"name": "original", "value": 10}
        print(f"Created record ID: {db.record_uuid}")

        db.output = {"name": "updated", "value": 20}
        print(f"Updated record")

    with SQLite(db_path) as db:
        total = db.count_records()
        print(f"Total records: {total}")

    if os.path.exists(db_path):
        os.remove(db_path)

    print("[OK] Example completed")


if __name__ == "__main__":
    main()