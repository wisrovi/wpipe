"""
10 SQLite - Transaction Handling

Shows transaction handling in SQLite.
"""

from wpipe.sqlite import SQLite
import os


def main():
    db_path = "transaction_test.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    db = SQLite(db_name=db_path)

    db.write(input_data={"step": 1}, output={"status": "started"})
    db.write(input_data={"step": 2}, output={"status": "completed"})

    count = db.count_records()
    print(f"Records after transaction: {count}")

    db.__exit__(None, None, None)

    if os.path.exists(db_path):
        os.remove(db_path)


if __name__ == "__main__":
    main()
