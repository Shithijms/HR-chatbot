from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.langchain.sql_agent import ask_query
from app.langchain_handler import generate_sql
from app.llm.query_parser import question_to_sql
import re
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.database import get_db
from langchain_groq import ChatGroq
import os

llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),  
    model_name="llama3-8b-8192"
)

router = APIRouter()

class QueryInput(BaseModel):
    question: str

class QueryRequest(BaseModel):
    question: str


def extract_sql(response: str) -> str:
    # Extract SQL code between triple backticks
    match = re.search(r"```sql\s*(.*?)```", response, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Fallback: first line starting with SELECT
    lines = response.strip().splitlines()
    for line in lines:
        if line.strip().lower().startswith("select"):
            return line.strip()

    return response.strip()


sql_prompt = PromptTemplate(
    input_variables=["question"],
    template="""
You are a SQL expert working with a MySQL database. Based on the user's question, write a syntactically correct SQL query.
Only provide the SQL query and nothing else unless clarification is needed.

Question: {question}
SQL:"""
)

llm_chain = LLMChain(prompt=sql_prompt, llm=llm)


@router.post("/ask")
def ask_hr_bot(request: QueryRequest):
    result = ask_query(request.question)
    return {"response": result}

@router.post("/ask-sql")
async def ask_sql(question_data: QueryRequest):
    question = question_data.question
    raw_response = llm_chain.invoke({"question": question})
    clean_sql = extract_sql(raw_response["text"])
    return {"sql_query": clean_sql}


@router.post("/query/ask")
async def ask(question: str):
    try:
        # Step 1: LLM generates response
        raw_response = llm_chain.invoke({"question": question})

        # Step 2: Extract the SQL query string
        sql = extract_sql(raw_response["text"])  

        # Step 3: Execute on the DB
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql)
        results = cursor.fetchall()

        return {
            "sql_query": sql,
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

