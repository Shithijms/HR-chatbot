from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq  
from dotenv import load_dotenv
import os
import re

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Load Groq LLM (LLaMA3)
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama3-8b-8192"
)

# HR Bot database schema as text
hr_bot_schema = """
-- departments(dept_id, name, manager_id)
-- employees(employee_id, name, email, gender, department_id, doj, employment_type, status)
-- leave_types(leave_type_id, name, max_days, is_paid, gender_restriction)
-- leave_balance(employee_id, leave_type_id, balance_days, last_updated)
-- leave_requests(leave_id, employee_id, leave_type_id, leave_date, reason, status, is_emergency, applied_on)
-- payroll(payroll_id, employee_id, month, gross_salary, net_salary)
-- hr_policies(policy_id, title, content, category, effective_from)
-- benefits(employee_id, benefit_type, provider, coverage_amt, valid_till)
-- attendance(employee_id, date, check_in_time, check_out_time, status)
-- holiday_calendar(holiday_date, name, region)
"""

# Updated prompt with schema
prompt = PromptTemplate(
    input_variables=["question"],
    template=f"""
You are an expert MySQL generator for an HR Bot system.

Use the following MySQL table schema:
{hr_bot_schema}

Your task: Convert the given question into a syntactically correct MySQL query that matches the schema. 
Do not explain anything. Just return the query.

Question: {{question}}

SQL Query:
"""
)

# Create the LLM chain
llm_chain = LLMChain(llm=llm, prompt=prompt)

# Main SQL generation function
def question_to_sql(question: str) -> str:
    try:
        response = llm_chain.run(question)
        return response.strip()
    except Exception as e:
        print("Error generating SQL:", e)
        return "ERROR"
