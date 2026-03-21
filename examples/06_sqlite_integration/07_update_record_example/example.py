"""
07 SQLite - Update Records

Shows updating existing records.
"""

from wpipe.sqlite import SQLite

def main():
    db = SQLite(db_name="update_test.db")
    
    record_id = db.write(input_data={"name": "original"}, output={"value": 0})
    db.update_record(record_id, output={"value": 100})
    
    record = db.read_by_id(record_id)
    print(f"Updated record: {record}")
    
    db.__exit__(None, None, None)

if __name__ == "__main__":
    main()
