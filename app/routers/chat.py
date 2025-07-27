from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import text
from app.database import SessionLocal
from app.llm.query_parser import question_to_sql
from sqlalchemy.orm import Session
from app.models import Employee, LeaveRequest, LeaveBalance
from app.database import get_db
import pymysql
from sqlalchemy import text
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import random

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

class ChatRequest(BaseModel):
    query: str

class LeaveRequestState(BaseModel):
    email: str
    leave_date: Optional[str] = None
    is_emergency: Optional[bool] = None
    reason: Optional[str] = None

class LeaveMessageRequest(BaseModel):
    message: str
    email: str


@router.post("/ask")
async def ask_chat(request: Request, db: Session = Depends(get_db)):
    try:
        body = await request.body()
        question = body.decode("utf-8").strip()

        sql = question_to_sql(question)

        if sql == "ERROR":
            return {"answer": "Sorry, I couldn't understand the question."}

        result = db.execute(text(sql)).fetchall()

        if not result:
            return {"answer": "No results found."}

        # Convert SQLAlchemy Row to dict
        readable = []
        for row in result:
            if isinstance(row, tuple):  # fallback: positional access
                readable.append(", ".join(str(col) for col in row))
            else:  # named column access
                readable.append(", ".join(f"{k}: {v}" for k, v in row._mapping.items()))

        return {"answer": " | ".join(readable)}

    except Exception as e:
        return {"answer": f"Error: {str(e)}"}


# In-memory state store (for demo, replace with Redis in prod)
session_states = {}

@router.post("/request-leave")
def handle_leave_flow(payload: LeaveMessageRequest, db: Session = Depends(get_db)):
    message = payload.message
    email = payload.email
    user_key = email.lower()

    if message.lower() == "exit":
        session_states.pop(user_key, None)
        return {"message": "Leave request process cancelled."}

    # Initialize state
    if message.lower() == "request leave":
        session_states[user_key] = LeaveRequestState(email=email)
        return {"message": "Is this an emergency leave? (yes/no)"}

    state = session_states.get(user_key)
    if not state:
        return {"message": "Type 'Request leave' to begin."}

    # Step 1: Emergency status
    if state.is_emergency is None:
        if message.lower() not in ["yes", "no"]:
            return {"message": "Please respond with 'yes' or 'no' for emergency."}
        state.is_emergency = message.lower() == "yes"

        # Check leave balance
        employee = db.query(Employee).filter(Employee.email == state.email).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        balance = db.query(LeaveBalance).filter(LeaveBalance.employee_id == employee.employee_id).first()
        if not balance or (balance.balance_days <= 0 and not state.is_emergency):
            session_states.pop(user_key, None)
            return {"message": "No leave balance available. Only emergency leaves allowed."}

        return {"message": "Please enter the leave date (YYYY-MM-DD):"}

    # Step 2: Leave Date
    if state.leave_date is None:
        try:
            datetime.strptime(message, "%Y-%m-%d")
            state.leave_date = message
        except ValueError:
            return {"message": "Invalid date format. Use YYYY-MM-DD"}
        return {"message": "Enter the reason for your leave:"}

    # Step 3: Reason
    if state.reason is None:
        state.reason = message

        # Fetch employee info again
        employee = db.query(Employee).filter(Employee.email == state.email).first()
        leave_balance = db.query(LeaveBalance).filter(LeaveBalance.employee_id == employee.employee_id).first()

        leave_request = LeaveRequest(
            employee_id=employee.employee_id,
            leave_type_id=leave_balance.leave_type_id,
            leave_date=state.leave_date,
            reason=state.reason,
            status="pending",
            is_emergency=state.is_emergency,
            applied_on=datetime.now()
        )

        db.add(leave_request)
        if not state.is_emergency:
            leave_balance.balance_days -= 1
        db.commit()

        session_states.pop(user_key, None)
        return {"message": "Leave request submitted successfully ✅"}

    return {"message": "Leave request already submitted. Type 'Request leave' to start again."}