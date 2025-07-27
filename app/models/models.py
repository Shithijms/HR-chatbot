from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, Boolean, DECIMAL, Text, Time
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Enum definitions
class GenderEnum(str, enum.Enum):
    M = "M"
    F = "F"
    Other = "Other"

class EmploymentTypeEnum(str, enum.Enum):
    FT = "FT"
    PT = "PT"
    Contract = "Contract"

class StatusEnum(str, enum.Enum):
    Active = "Active"
    Resigned = "Resigned"
    OnLeave = "On Leave"

class LeaveStatusEnum(str, enum.Enum):
    Pending = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"

class GenderRestrictionEnum(str, enum.Enum):
    M = "M"
    F = "F"
    All = "All"

# 1. Departments
class Department(Base):
    __tablename__ = "departments"

    dept_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    manager_id = Column(Integer, nullable=True)

# 2. Employees
class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    gender = Column(Enum(GenderEnum))
    department_id = Column(Integer, ForeignKey("departments.dept_id"))
    doj = Column(Date)
    employment_type = Column(Enum(EmploymentTypeEnum))
    status = Column(Enum(StatusEnum))

# 3. Leave Types
class LeaveType(Base):
    __tablename__ = "leave_types"

    leave_type_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    max_days = Column(Integer)
    is_paid = Column(Boolean)
    gender_restriction = Column(Enum(GenderRestrictionEnum), default=GenderRestrictionEnum.All)

# 4. Leave Balance
class LeaveBalance(Base):
    __tablename__ = "leave_balance"

    employee_id = Column(Integer, ForeignKey("employees.employee_id"), primary_key=True)
    leave_type_id = Column(Integer, ForeignKey("leave_types.leave_type_id"), primary_key=True)
    balance_days = Column(DECIMAL(4,1))
    last_updated = Column(Date)

# 5. Leave Requests
class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    leave_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    leave_type_id = Column(Integer, ForeignKey("leave_types.leave_type_id"))
    leave_date = Column(Date)
    reason = Column(Text)
    status = Column(Enum(LeaveStatusEnum))
    is_emergency = Column(Boolean, default=False)
    applied_on = Column(Date)

# 6. Payroll
class Payroll(Base):
    __tablename__ = "payroll"

    payroll_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    month = Column(Date)
    gross_salary = Column(DECIMAL(10,2))
    net_salary = Column(DECIMAL(10,2))

# 7. HR Policies
class HRPolicy(Base):
    __tablename__ = "hr_policies"

    policy_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    content = Column(Text)
    category = Column(String(100))
    effective_from = Column(Date)

# 8. Benefits
class Benefit(Base):
    __tablename__ = "benefits"

    employee_id = Column(Integer, ForeignKey("employees.employee_id"), primary_key=True)
    benefit_type = Column(String(100), primary_key=True)
    provider = Column(String(100))
    coverage_amt = Column(DECIMAL(10,2))
    valid_till = Column(Date)

# 9. Attendance
class Attendance(Base):
    __tablename__ = "attendance"

    employee_id = Column(Integer, ForeignKey("employees.employee_id"), primary_key=True)
    date = Column(Date, primary_key=True)
    check_in_time = Column(Time)
    check_out_time = Column(Time)
    status = Column(Enum("Present", "Absent", "WFH", "Leave", name="attendance_status"))

# 10. Holiday Calendar
class Holiday(Base):
    __tablename__ = "holiday_calendar"

    holiday_date = Column(Date, primary_key=True)
    name = Column(String(100))
    region = Column(String(100))
