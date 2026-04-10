from wpipe.sqlite import SQLite
import tempfile
import os

with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
    db_path = f.name

try:
    db = SQLite(db_path)
    rid = db.write(input_data={"test": "value"})
    print(f"Inserted ID: {rid}")
    
    record = db.read_by_id(rid)
    print(f"Read record: {record}")
    
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(f"Tables: {cursor.fetchall()}")
    
    cursor = conn.execute("SELECT * FROM recordmodel")
    print(f"Rows in recordmodel: {cursor.fetchall()}")
finally:
    if os.path.exists(db_path):
        os.remove(db_path)
