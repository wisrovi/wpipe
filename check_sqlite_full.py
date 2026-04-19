from wpipe.sqlite import SQLite
import tempfile
import os
from wsqlite import WSQLite
from wpipe.sqlite.tables_dto.records import RecordModel

with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
    db_path = f.name

try:
    # Use standard WPipe SQLite wrapper
    db = SQLite(db_path)
    rid = db.write(input_data={"test": "performance"})
    print(f"Inserted ID: {rid}")
    
    record = db.read_by_id(rid)
    print(f"Read record: {record}")
    
    # Inspection using pure WSQLite (No sqlite3 import)
    inspector = WSQLite(RecordModel, db_path)
    all_rows = inspector.get_all()
    print(f"Rows found via WSQLite: {len(all_rows)}")
    for row in all_rows:
        print(f" - Data: {row.input_data}")

finally:
    if os.path.exists(db_path):
        os.remove(db_path)
