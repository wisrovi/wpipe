from wsqlite import WSQLite
from pydantic import BaseModel
from typing import Optional

class M(BaseModel):
    id: Optional[int] = None
    data: Optional[str] = None

db = WSQLite(M, "temp.db")
print(dir(db))
