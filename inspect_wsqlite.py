"""
Module to inspect the WSQLite database instance.

This script demonstrates how to instantiate the WSQLite wrapper and
inspect its structure and available attributes.
"""

from typing import Optional
from pydantic import BaseModel
from wsqlite import WSQLite

class InspectorModel(BaseModel):
    """
    Model for database inspection.

    Attributes:
        id: Optional integer representing the unique identifier.
        data: Optional string containing data.
    """
    id: Optional[int] = None
    data: Optional[str] = None

def inspect_database() -> None:
    """
    Perform an inspection on a temporary WSQLite database.
    """
    db_instance: WSQLite = WSQLite(InspectorModel, "temp.db")
    print(dir(db_instance))

if __name__ == "__main__":
    inspect_database()
