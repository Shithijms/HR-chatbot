from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()  

# Initialize Groq LLM
llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),  
    model_name="llama3-8b-8192"
)

# Prompt Template
prompt = PromptTemplate(
    input_variables=["schema", "question"],
    template="""
You are an assistant that converts questions into SQL queries.
Assume the following schema:
{schema}

Question: {question}

SQL Query:
"""
)

# Chain
chain = LLMChain(llm=llm, prompt=prompt)

# Function to get SQL
def generate_sql(schema: str, question: str) -> str:
    return chain.run(schema=schema, question=question)
