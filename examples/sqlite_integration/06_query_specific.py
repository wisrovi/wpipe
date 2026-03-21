"""
06 SQLite - Query Specific Records

Shows querying specific records by ID.
"""

from wpipe.sqlite import SQLite

def main():
    db = SQLite(db_name="query_test.db")
    
    id1 = db.write(input_data={"name": "test1"}, output={"value": 1})
    id2 = db.write(input_data={"name": "test2"}, output={"value": 2})
    
    record = db.read_by_id(id1)
    print(f"Record 1: {record}")
    
    db.__exit__(None, None, None)

if __name__ == "__main__":
    main()
