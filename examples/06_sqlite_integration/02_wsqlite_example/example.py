"""
02 SQLite - Using Wsqlite Context Manager

Shows using Wsqlite for convenient context manager usage.
"""

import os

from wpipe.sqlite import Wsqlite


def main() -> None:
    """Run the Wsqlite context manager example.

    Uses Wsqlite as a context manager to set input and output data
    on records with automatic cleanup on exit.
    """
    db_path: str = "test_wsqlite.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    with Wsqlite(db_name=db_path) as db:
        db.input = {"name": "pipeline_run", "id": 123}
        print(f"Input set, record ID: {db.id}")

        db.output = {"result": "completed", "value": 42}
        print(f"Output set, record ID: {db.id}")

        print(f"Total records: {db.count_records()}")

    if os.path.exists(db_path):
        os.remove(db_path)


if __name__ == "__main__":
    main()
