"""
01 SQLite - Basic Write and Read

The simplest SQLite example - writing and reading data.
"""

from wpipe.sqlite import SQLite
import os


def main():
    db_path = "test_basic.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    db = SQLite(db_name=db_path)

    record_id = db.write(
        input_data={"name": "test", "value": 100}, output={"result": "success"}
    )

    print(f"Written record ID: {record_id}")

    records = db.read_by_id(record_id)
    print(f"Read record: {records}")

    count = db.count_records()
    print(f"Total records: {count}")

    db.__exit__(None, None, None)

    if os.path.exists(db_path):
        os.remove(db_path)


if __name__ == "__main__":
    main()
