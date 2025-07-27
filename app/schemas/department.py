from typing import Optional
from pydantic import BaseModel

class DepartmentCreate(BaseModel):
    name: str
    manager_id: int | None = None

class DepartmentOut(DepartmentCreate):
    dept_id: int
    name: str
    manager_id: Optional[int]

    model_config = {
        "from_attributes":True
    }
