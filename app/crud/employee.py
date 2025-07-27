from sqlalchemy.orm import Session
from app.models.models import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate

def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.employee_id == employee_id).first()


# 1. Get all employees
def get_all_employees(db: Session):
    return db.query(Employee).all()

# 2. Get employee by ID
def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.employee_id == employee_id).first()

# 3. Update employee
def update_employee(db: Session, employee_id: int, updated_data: EmployeeUpdate):
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not employee:
        return None
    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return employee

# 4. Delete employee
def delete_employee(db: Session, employee_id: int):
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not employee:
        return None
    db.delete(employee)
    db.commit()
    return employee

# 5. Get employees by department
def get_employees_by_department(db: Session, dept_id: int):
    return db.query(Employee).filter(Employee.department_id == dept_id).all()