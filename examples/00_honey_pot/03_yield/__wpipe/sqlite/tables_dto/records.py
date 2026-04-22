from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RecordModel(BaseModel):
    """DTO for the records table in SQLite."""

    id: Optional[int] = Field(None, description="Primary Key")
    input: Optional[str] = Field(None, description="Input data as JSON string")
    output: Optional[str] = Field(None, description="Output data as JSON string")
    details: Optional[str] = Field(
        None, description="Additional details as JSON string"
    )
    datetime: Optional[str] = Field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
