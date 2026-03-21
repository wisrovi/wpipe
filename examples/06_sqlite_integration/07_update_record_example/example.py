"""
07 SQLite - Update Records

Shows updating existing records.
"""

from wpipe.sqlite import SQLite


def main() -> None:
    """Run the update records example.

    Creates a SQLite database, writes a record, updates its output
    data, and reads the record to verify the update.
    """
    db: SQLite = SQLite(db_name="update_test.db")

    record_id: int = db.write(input_data={"name": "original"}, output={"value": 0})
    db.update_record(record_id, output={"value": 100})

    record: dict = db.read_by_id(record_id)
    print(f"Updated record: {record}")

    db.__exit__(None, None, None)


if __name__ == "__main__":
    main()
