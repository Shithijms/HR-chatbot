from pydantic import BaseModel
from datetime import date, time

class AttendanceBase(BaseModel):
    employee_id: int
    date: date
    check_in: time
    check_out: time

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceOut(AttendanceBase):
    attendance_id: int

    class Config:
        from_attributes = True  # For Pydantic v2 (equivalent to orm_mode=True in v1)
