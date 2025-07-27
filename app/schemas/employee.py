from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional, Literal

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    gender: Literal['M', 'F', 'Other']
    department_id: int
    doj: date
    employment_type: Literal['FT', 'PT', 'Contract']
    status: Literal['Active', 'Resigned', 'On Leave']

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeOut(EmployeeBase):
    employee_id: int

    class Config:
        orm_mode = True

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: Optional[Literal['M', 'F', 'Other']] = None
    department_id: Optional[int] = None
    doj: Optional[date] = None
    employment_type: Optional[Literal['FT', 'PT', 'Contract']] = None
    status: Optional[Literal['Active', 'Resigned', 'On Leave']] = None
