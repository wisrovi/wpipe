"""
03 SQLite - Export to CSV

Shows exporting database contents to CSV manually.
"""

import os
import csv
import json

from wpipe.sqlite import SQLite


def main() -> None:
    """Run the export to CSV example.

    Creates multiple records in a SQLite database and exports to CSV.
    """
    db_path: str = "test_export.db"
    csv_path: str = "export.csv"
    if os.path.exists(db_path):
        os.remove(db_path)
    if os.path.exists(csv_path):
        os.remove(csv_path)

    db: SQLite = SQLite(db_name=db_path)

    for i in range(5):
        db.write(input_data={"index": i}, output={"value": i * 10})

    records = []
    for i in range(1, db.count_records() + 1):
        rec = db.read_by_id(i)
        records.append(rec)

    print("Records:")
    for rec in records:
        print(f"  {rec}")

    with open(csv_path, 'w', newline='') as f:
        if records:
            writer = csv.DictWriter(f, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)

    print(f"\nExported to: {csv_path}")
    print(f"Total records: {db.count_records()}")

    db.__exit__(None, None, None)

    if os.path.exists(db_path):
        os.remove(db_path)
    if os.path.exists(csv_path):
        os.remove(csv_path)


if __name__ == "__main__":
    main()