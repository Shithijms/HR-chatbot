
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Employee
from pydantic import BaseModel

router = APIRouter()

class EmailRequest(BaseModel):
    email: str

@router.post("/auth/validate-email")
async def validate_email(data: EmailRequest, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.email == data.email).first()
    if employee:
        return {"success": True, "message": f"Email is {data.email}"}
    else:
        raise HTTPException(status_code=401, detail="Email not found")
