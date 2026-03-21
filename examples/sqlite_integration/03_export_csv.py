"""
03 SQLite - Export to CSV

Shows exporting database contents to CSV.
"""

from wpipe.sqlite import SQLite
import os


def main():
    db_path = "test_export.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    db = SQLite(db_name=db_path)

    for i in range(5):
        db.write(input={"index": i}, output={"value": i * 10})

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
