"""
03 SQLite - Export to CSV

Shows exporting database contents to CSV.
"""

import os

from wpipe.sqlite import SQLite


def main() -> None:
    """Run the export to CSV example.

    Creates multiple records in a SQLite database, exports all records
    to a pandas DataFrame, and saves the data to a CSV file.
    """
    db_path: str = "test_export.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    db: SQLite = SQLite(db_name=db_path)

    for i in range(5):
        db.write(input_data={"index": i}, output={"value": i * 10})

    df = db.export_to_dataframe(save_csv=True, csv_name="export.csv")

    print("DataFrame:")
    print(df)

    print(f"\nTotal records: {db.count_records()}")

    db.__exit__(None, None, None)

    if os.path.exists(db_path):
        os.remove(db_path)
    if os.path.exists("export.csv"):
        os.remove("export.csv")


if __name__ == "__main__":
    main()
