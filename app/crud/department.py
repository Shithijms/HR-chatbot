from sqlalchemy.orm import Session
from app.models.models import Department
from app.schemas.department import DepartmentCreate, DepartmentOut

def get_all_departments(db: Session):
    return db.query(Department).all()

def get_department(db: Session, dept_id: int):
    return db.query(Department).filter(Department.dept_id == dept_id).first()

def create_department(db: Session, dept: DepartmentCreate):
    new_dept = Department(**dept.dict())
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    return new_dept

def update_department(db: Session, dept_id: int, dept: DepartmentCreate):
    existing = db.query(Department).filter(Department.dept_id == dept_id).first()
    if not existing:
        return None
    for key, value in dept.dict().items():
        setattr(existing, key, value)
    db.commit()
    db.refresh(existing)
    return existing

def delete_department(db: Session, dept_id: int):
    dept = db.query(Department).filter(Department.dept_id == dept_id).first()
    if dept:
        db.delete(dept)
        db.commit()
    return dept
