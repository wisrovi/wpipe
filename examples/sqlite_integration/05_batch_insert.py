"""
05 SQLite - Batch Insert

Shows inserting multiple records in batch.
"""

from wpipe.sqlite import SQLite

def main():
    db = SQLite(db_name="batch_test.db")
    
    for i in range(10):
        db.write(input_data={"index": i}, output={"value": i * 10})
    
    count = db.count_records()
    print(f"Total records: {count}")
    db.__exit__(None, None, None)

if __name__ == "__main__":
    main()
