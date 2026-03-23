"""
08 SQLite - Delete Records

Shows deleting records from database.
"""

from wpipe.sqlite import SQLite


def main() -> None:
    """Run the delete records example.

    Creates a SQLite database, writes two records, deletes one of them,
    and counts remaining records to verify deletion.
    """
    db: SQLite = SQLite(db_name="delete_test.db")

    db.write(input_data={"name": "keep"}, output={"value": 1})
    id2: int = db.write(input_data={"name": "delete"}, output={"value": 2})

    db.delete_by_id(id2)

    count: int = db.count_records()
    print(f"Remaining records: {count}")

    db.__exit__(None, None, None)


if __name__ == "__main__":
    main()
