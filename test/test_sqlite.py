import os
import json
import pytest
from wpipe.sqlite.Sqlite import Wsqlite, SQLite

@pytest.fixture
def wsqlite_db(tmp_path):
    db_path = str(tmp_path / "test_wsqlite.db")
    with Wsqlite(db_name=db_path) as db:
        yield db
    if os.path.exists(db_path):
        os.remove(db_path)

def test_wsqlite_properties_and_save(wsqlite_db):
    assert wsqlite_db.count_records() == 0
    
    # Test setters that trigger _save_state
    wsqlite_db.input = {"test_in": "value"}
    assert wsqlite_db.input == {"test_in": "value"}
    
    wsqlite_db.output = {"test_out": "value2"}
    assert wsqlite_db.output == {"test_out": "value2"}
    
    wsqlite_db.details = {"info": "some details"}
    assert wsqlite_db.details == {"info": "some details"}
    
    wsqlite_db.error = {"msg": "error details"}
    assert wsqlite_db.error == {"msg": "error details"}
    
    # We should have exactly 1 record after all these updates (upsert logic)
    assert wsqlite_db.count_records() == 1

def test_wsqlite_context_manager(tmp_path):
    db_path = str(tmp_path / "test_wsqlite_ctx.db")
    with Wsqlite(db_name=db_path) as db:
        db.input = {"a": 1}
    
    # Check if saved
    with Wsqlite(db_name=db_path) as db2:
        assert db2.count_records() == 1

@pytest.fixture
def sqlite_db(tmp_path):
    db_path = str(tmp_path / "test_sqlite.db")
    with SQLite(db_name=db_path) as db:
        yield db
    if os.path.exists(db_path):
        os.remove(db_path)

def test_sqlite_write_and_read(sqlite_db):
    assert sqlite_db.count_records() == 0
    
    # Test writing new record
    record_id = sqlite_db.write(
        input_data={"in": 1},
        output={"out": 2},
        details={"det": 3}
    )
    assert record_id is not None
    assert sqlite_db.count_records() == 1
    
    # Test reading
    read_data = sqlite_db.read_by_id(record_id)
    assert read_data is not None
    assert read_data["id"] == record_id
    assert json.loads(read_data["input"]) == {"in": 1}
    assert json.loads(read_data["output"]) == {"out": 2}
    assert json.loads(read_data["details"]) == {"det": 3}
    
    # Test updating existing record
    sqlite_db.write(
        input_data={"in": "updated"},
        output={"out": "updated"},
        details={"det": "updated"},
        record_id=record_id
    )
    
    read_data_updated = sqlite_db.read_by_id(record_id)
    assert json.loads(read_data_updated["input"]) == {"in": "updated"}
    assert sqlite_db.count_records() == 1

def test_sqlite_write_formats(sqlite_db):
    # Test writing with string output
    record_id1 = sqlite_db.write(output="just string")
    read1 = sqlite_db.read_by_id(record_id1)
    assert json.loads(read1["output"]) == {"output": "just string"}
    
    # Test writing with no output
    record_id2 = sqlite_db.write(input_data="string_input", output=None)
    read2 = sqlite_db.read_by_id(record_id2)
    assert read2["input"] == "string_input"
    assert read2["output"] is None

def test_sqlite_read_non_existent(sqlite_db):
    assert sqlite_db.read_by_id(999) is None
