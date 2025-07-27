from fastapi import APIRouter, Depends, HTTPException
from app.crud import attendance as crud
from sqlalchemy.orm import Session
from app.database import *
from app.schemas.department import DepartmentCreate, DepartmentOut
from app.crud import department as crud
from app.models import models
from app.schemas.attendance import AttendanceBase, AttendanceCreate, AttendanceOut

@router.post("/", response_model=AttendanceOut)
def create_attendance_route(attendance_data: AttendanceCreate, db: Session = Depends(get_db)):
    return crud.create_attendance(db, attendance_data)

@router.get("/{attendance_id}", response_model=AttendanceOut)
def get_attendance(attendance_id: int, db: Session = Depends(get_db)):
    attendance = crud.get_attendance_by_id(db, attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return attendance

@router.get("/employee/{employee_id}", response_model=list[AttendanceOut])
def get_attendance_by_employee(employee_id: int, db: Session = Depends(get_db)):
    return crud.get_attendance_by_employee(db, employee_id)

@router.put("/{attendance_id}", response_model=AttendanceOut)
def update_attendance_route(attendance_id: int, updated_data: AttendanceCreate, db: Session = Depends(get_db)):
    attendance = crud.update_attendance(db, attendance_id, updated_data)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return attendance

@router.delete("/{attendance_id}")
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    attendance = crud.delete_attendance(db, attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return {"message": "Attendance deleted"}


