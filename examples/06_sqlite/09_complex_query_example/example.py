"""
07 SQLite - Complex Query

Shows complex query patterns.
"""

import os

from wpipe.sqlite import Wsqlite, SQLite


def main() -> None:
    """Run complex query example."""
    db_path: str = "test_complex.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    for i in range(5):
        with Wsqlite(db_path) as db:
            db.input = {"index": i, "category": ["A", "B", "A"][i % 3]}

    with SQLite(db_path) as db:
        total = db.count_records()
        print(f"Total records: {total}")

        for i in range(1, total + 1):
            rec = db.read_by_id(i)
            print(f"  Record {i}: {rec.get('input')}")

    if os.path.exists(db_path):
        os.remove(db_path)

    print("[OK] Example completed")


if __name__ == "__main__":
    main()