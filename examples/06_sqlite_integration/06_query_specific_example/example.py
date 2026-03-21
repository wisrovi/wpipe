"""
06 SQLite - Query Specific Records

Shows querying specific records by ID.
"""

from wpipe.sqlite import SQLite


def main() -> None:
    """Run the query specific records example.

    Creates a SQLite database, writes multiple records, and queries
    a specific record by its ID.
    """
    db: SQLite = SQLite(db_name="query_test.db")

    id1: int = db.write(input_data={"name": "test1"}, output={"value": 1})
    db.write(input_data={"name": "test2"}, output={"value": 2})

    record: dict = db.read_by_id(id1)
    print(f"Record 1: {record}")

    db.__exit__(None, None, None)


if __name__ == "__main__":
    main()
