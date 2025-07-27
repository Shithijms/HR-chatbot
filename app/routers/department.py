from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import *
from app.schemas.department import DepartmentCreate, DepartmentOut
from app.crud import department as crud
from app.models import models

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)

@router.get("/departments", response_model=list[DepartmentOut])
def get_departments(db: Session = Depends(get_db)):
    return crud.get_all_departments(db)

@router.get("/departments/{dept_id}", response_model=DepartmentOut)
def get_department(dept_id: int, db: Session = Depends(get_db)):
    dept = crud.get_department(db, dept_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

@router.post("/departments", response_model=DepartmentOut)
def create_department(dept: DepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_department(db, dept)

@router.put("/departments/{dept_id}", response_model=DepartmentOut)
def update_department(dept_id: int, dept: DepartmentCreate, db: Session = Depends(get_db)):
    updated = crud.update_department(db, dept_id, dept)
    if not updated:
        raise HTTPException(status_code=404, detail="Department not found")
    return updated

@router.delete("/departments/{dept_id}")
def delete_department(dept_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_department(db, dept_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Department not found")
    return {"message": "Department deleted successfully"}



# GET all departments
@router.get("/", response_model=list[DepartmentOut])
def get_departments(db: Session = Depends(get_db)):
    """
    Fetches all departments from the database.
    """
    return db.query(models.Department).all()


# POST a new department
@router.post("/", response_model=DepartmentOut)
def create_department(dept: DepartmentCreate, db: Session = Depends(get_db)):
    """
    Adds a new department using data from the request body.
    """
    new_dept = models.Department(name=dept.name, manager_id=dept.manager_id)
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    return new_dept