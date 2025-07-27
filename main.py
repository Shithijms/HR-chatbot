from fastapi import FastAPI
from app.database import engine
from app.models import models 
from app.database import create_tables
from app.routers import auth, department, employee
from dotenv import load_dotenv
from app.routers import department, employee, query , chat
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "HR Bot is running"}

app.include_router(department.router, prefix="/departments")
app.include_router(employee.router, prefix="/employees")
app.include_router(query.router, prefix="/query")  
app.include_router(chat.router, prefix="/chat")
app.include_router(auth.router)

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully.")
