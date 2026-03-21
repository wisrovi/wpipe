"""
10 SQLite - JSON Storage

Shows storing complex JSON data.
"""

from wpipe.sqlite import SQLite

def main():
    db = SQLite(db_name="json_test.db")
    
    complex_data = {
        "user": {"name": "John", "email": "john@test.com"},
        "items": [{"id": 1, "qty": 5}, {"id": 2, "qty": 10}]
    }
    
    record_id = db.write(input_data=complex_data, output={"status": "saved"})
    
    record = db.read_by_id(record_id)
    print(f"Stored record ID: {record_id}")
    
    db.__exit__(None, None, None)

if __name__ == "__main__":
    main()
