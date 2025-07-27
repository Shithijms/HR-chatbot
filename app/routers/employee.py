from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine
from app.database import SessionLocal
from app.schemas.employee import EmployeeCreate, EmployeeOut, EmployeeUpdate
from app.crud import employee as crud_employee

router = APIRouter(prefix="/employees", tags=["Employees"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=EmployeeOut)
def create_employee_api(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return crud_employee.create_employee(db, employee)

@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee_api(employee_id: int, db: Session = Depends(get_db)):
    employee = crud_employee.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


# Get all employees
@router.get("/employees", response_model=list[EmployeeOut])
def read_employees(db: Session = Depends(get_db)):
    return crud_employee.get_all_employees(db)

# Get employee by ID
@router.get("/employees/{employee_id}", response_model=EmployeeOut)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = crud_employee.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

# Update employee
@router.put("/employees/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: int, updated: EmployeeUpdate, db: Session = Depends(get_db)):
    emp = crud_employee.update_employee(db, employee_id, updated)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

# Delete employee
@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = crud_employee.delete_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}

# Get employees by department
@router.get("/departments/{dept_id}/employees", response_model=list[EmployeeOut])
def get_dept_employees(dept_id: int, db: Session = Depends(get_db)):
    return crud_employee.get_employees_by_department(db, dept_id)