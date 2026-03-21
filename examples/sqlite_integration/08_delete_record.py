"""
08 SQLite - Delete Records

Shows deleting records from database.
"""

from wpipe.sqlite import SQLite

def main():
    db = SQLite(db_name="delete_test.db")
    
    id1 = db.write(input_data={"name": "keep"}, output={"value": 1})
    id2 = db.write(input_data={"name": "delete"}, output={"value": 2})
    
    db.delete_record(id2)
    
    count = db.count_records()
    print(f"Remaining records: {count}")
    
    db.__exit__(None, None, None)

if __name__ == "__main__":
    main()
