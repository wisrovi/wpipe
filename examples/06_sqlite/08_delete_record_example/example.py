"""
06 SQLite - Delete Records

Shows deleting records in SQLite.
"""

import os

from wpipe.sqlite import Wsqlite, SQLite


def main() -> None:
    """Run delete example."""
    db_path: str = "test_delete.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    uuids = []
    for i in range(3):
        with Wsqlite(db_path) as db:
            db.input = {"index": i}
            uuids.append(db.record_uuid)
            print(f"Created record: {db.record_uuid}")

    with SQLite(db_path) as db:
        print(f"Total records: {db.count_records()}")

    if os.path.exists(db_path):
        os.remove(db_path)

    print("[OK] Example completed")


if __name__ == "__main__":
    main()