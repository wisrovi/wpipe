import json
import os
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from typing import Literal
from datetime import datetime
import pandas as pd


class SQLite:
    def __init__(self, db_name: str = "register.db"):
        # nombre absoluto de db_name
        # self.db_name = os.path.basename(db_name)
        self.db_name = db_name
        self._create_table_if_not_exists()

        self.executor = ThreadPoolExecutor(max_workers=10)

    def _create_table_if_not_exists(self):
        if not self.db_name:
            return

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS records
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                               input TEXT,
                               output TEXT,
                               details TEXT DEFAULT NULL,
                               datetime TEXT DEFAULT CURRENT_TIMESTAMP)"""
            )

    def async_write(
        self, input: str = None, output: str = None, details: str = None, id: int = None
    ):
        self.executor.submit(self.write, input, output, details, id)

    def write(
        self,
        input: str = None,
        output: Literal["str", "dict"] = None,
        details: str = None,
        id: int = None,
    ):
        if not self.check_table_exists():
            return

        if isinstance(input, dict):
            input = json.dumps(input)

        if isinstance(output, dict):
            output["datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            output = json.dumps(output)

        elif isinstance(output, str):
            output = json.dumps(
                {
                    "output": output,
                    "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

        if isinstance(details, dict):
            details = json.dumps(details)

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            if not id:
                # insert
                cursor.execute(
                    "INSERT INTO records (input, output, details) VALUES (?, ?, ?)",
                    (input, output, details),
                )

                id = cursor.lastrowid
            else:
                # update
                if not self.read_by_id(id):
                    return

                if not input and not details and output:
                    cursor.execute(
                        "UPDATE records SET output = ? WHERE id = ?",
                        (output, id),
                    )
                elif not input and output and details:
                    cursor.execute(
                        "UPDATE records SET output = ?, details = ? WHERE id = ?",
                        (output, details, id),
                    )
                elif input and output and details:
                    cursor.execute(
                        "UPDATE records SET input = ?, output = ?, details = ? WHERE id = ?",
                        (input, output, details, id),
                    )
                elif input and output and not details:
                    cursor.execute(
                        "UPDATE records SET input = ?, output = ? WHERE id = ?",
                        (input, output, id),
                    )
            conn.commit()

        return id

    def read_by_id(self, id: int) -> list:
        if not self.check_table_exists():
            return []

        results = []

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM records WHERE id = ?", (id,))

            results = cursor.fetchall()

            if cursor.rowcount == 0:
                # print("No records found for the specified id")
                pass

        return results

    def _view_records(self) -> pd.DataFrame:
        with sqlite3.connect(self.db_name) as conn:
            return pd.read_sql_query("SELECT * FROM records", conn)

    def export_to_dataframe(
        self, save_csv: bool = False, csv_name: str = "records.csv"
    ) -> pd.DataFrame:
        if not self.check_table_exists():
            return pd.DataFrame()

        df = self._view_records()

        if save_csv:
            df.to_csv(csv_name, index=False)

        return df

    def get_records_by_date_range(self, start_date: str, end_date: str) -> list:
        if not self.check_table_exists():
            return []

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM records WHERE datetime BETWEEN ? AND ?",
                (start_date, end_date),
            )
            return cursor.fetchall()

    def count_records(self) -> int:
        if not self.check_table_exists():
            return 0

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM records")
            return cursor.fetchone()[0]

    def delete_by_id(self, id_saved: int):
        if not self.check_table_exists():
            return

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM records WHERE id = ?", (id_saved,))
            conn.commit()

    def check_table_exists(self) -> bool:
        if not self.db_name:
            return False

        if len(os.path.dirname(self.db_name)) > 0:
            if not os.path.exists(os.path.dirname(self.db_name)):
                os.makedirs(os.path.dirname(self.db_name))

        self._create_table_if_not_exists()

        return True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.executor:
            self.executor.shutdown(wait=True)


if __name__ == "__main__":
    import uuid

    my_uuid = str(uuid.uuid4().hex)

    with SQLite() as registro:
        registro.write(topic="topic 1", type_data="image", value=my_uuid)
        registro.write(topic="topic 2", type_data="image", value=my_uuid)
        registro.write(topic="topic 3", type_data="image", value=my_uuid)
        registro.write(topic="topic 4", type_data="image", value=my_uuid)

        print(registro.read_by_id(str(uuid.uuid4().hex)))

        print(registro.export_to_dataframe().head())

        print("total", registro.count_records())
