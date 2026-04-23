"""
Module to check the WSQLite functionality.

This script demonstrates basic insertion operations using the WSQLite database wrapper
with a Pydantic model.
"""

from typing import Optional
from pydantic import BaseModel, Field
from wsqlite import WSQLite

class TestModel(BaseModel):
    """
    Test Pydantic model for database checking.

    Attributes:
        id: Optional integer representing the primary key.
        data: String containing the data to be stored.
    """
    id: Optional[int] = Field(None, description="Primary Key")
    data: str

def check_database() -> None:
    """
    Execute a check on the WSQLite database insertion.
    """
    db_instance: WSQLite = WSQLite(TestModel, "test_check.db")
    test_entry: TestModel = TestModel(data="hello")
    res: int = db_instance.insert(test_entry)
    print(f"Insert result: {res}")

if __name__ == "__main__":
    check_database()
