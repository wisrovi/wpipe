"""
DTO models for pipeline record entries in SQLite.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RecordModel(BaseModel):
    """
    Data Transfer Object for the records table in SQLite.

    Attributes:
        id (Optional[int]): Primary Key of the record.
        input (Optional[str]): Input data stored as a JSON string.
        output (Optional[str]): Output data stored as a JSON string.
        details (Optional[str]): Additional execution details stored as a JSON string.
        datetime (Optional[str]): Timestamp of the record creation.
    """

    id: Optional[int] = Field(None, description="Primary Key")
    input: Optional[str] = Field(None, description="Input data as JSON string")
    output: Optional[str] = Field(None, description="Output data as JSON string")
    details: Optional[str] = Field(
        None, description="Additional details as JSON string"
    )
    datetime: Optional[str] = Field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
