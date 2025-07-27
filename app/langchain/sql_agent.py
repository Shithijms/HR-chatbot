from langchain_groq import ChatGroq  
from langchain_experimental.sql import SQLDatabaseChain
from langchain.sql_database import SQLDatabase
from sqlalchemy import create_engine
import os

db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "3306")
db_name = os.getenv("DB_NAME", "hr_bot")

db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


# Initialize components
engine = create_engine(db_url)
db = SQLDatabase(engine)

#  Groq LLM 
llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),  
    model_name="llama3-8b-8192"
)

sql_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

def ask_query(natural_question: str) -> str:
    response = sql_chain.invoke(natural_question)  
    return response
