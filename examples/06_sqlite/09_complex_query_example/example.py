"""
09 SQLite - Complex Query

Shows complex query with date range.
"""

from wpipe.sqlite import SQLite


def main() -> None:
    """Run the complex query example.

    Creates a SQLite database, writes multiple records, and queries
    records within a specific date range.
    """
    db: SQLite = SQLite(db_name="complex_test.db")

    for i in range(5):
        db.write(input_data={"index": i}, output={"value": i})

    records: list[dict] = db.get_records_by_date_range(days=1)
    print(f"Records in range: {len(records)}")

    db.__exit__(None, None, None)


if __name__ == "__main__":
    main()
