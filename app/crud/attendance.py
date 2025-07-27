from sqlalchemy.orm import Session
from app import models, schemas

def create_attendance(db: Session, attendance: schemas.AttendanceCreate):
    db_attendance = models.Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def get_all_attendance(db: Session):
    return db.query(models.Attendance).all()

def get_attendance_by_employee(db: Session, employee_id: int):
    return db.query(models.Attendance).filter(models.Attendance.employee_id == employee_id).all()

def update_attendance(db: Session, attendance_id: int, updated_data: schemas.AttendanceCreate):
    attendance = db.query(models.Attendance).filter(models.Attendance.attendance_id == attendance_id).first()
    if attendance:
        for key, value in updated_data.model_dump().items():
            setattr(attendance, key, value)
        db.commit()
        db.refresh(attendance)
    return attendance

def delete_attendance(db: Session, attendance_id: int):
    attendance = db.query(models.Attendance).filter(models.Attendance.attendance_id == attendance_id).first()
    if attendance:
        db.delete(attendance)
        db.commit()
    return attendance
