from wsqlite import WSQLite
from pydantic import BaseModel, Field
from typing import Optional

class TestModel(BaseModel):
    id: Optional[int] = Field(None, description="Primary Key")
    data: str

db = WSQLite(TestModel, "test_check.db")
res = db.insert(TestModel(data="hello"))
print(f"Insert result: {res}")
