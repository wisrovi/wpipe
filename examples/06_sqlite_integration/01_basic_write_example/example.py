"""
01 SQLite - Basic Write and Read

The simplest SQLite example - writing and reading data.
"""

import os

from wpipe.sqlite import SQLite


def main() -> None:
    """Run the basic write and read example.

    Creates a SQLite database, writes a record with input and output data,
    reads the record back by ID, and counts total records.
    """
    db_path: str = "test_basic.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    db: SQLite = SQLite(db_name=db_path)

    record_id: int = db.write(
        input_data={"name": "test", "value": 100}, output={"result": "success"}
    )

    print(f"Written record ID: {record_id}")

    records: dict = db.read_by_id(record_id)
    print(f"Read record: {records}")

    count: int = db.count_records()
    print(f"Total records: {count}")

    db.__exit__(None, None, None)

    if os.path.exists(db_path):
        os.remove(db_path)


if __name__ == "__main__":
    main()
