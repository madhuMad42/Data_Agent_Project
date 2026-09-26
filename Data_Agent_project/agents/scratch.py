import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.llm_pick import pick_llm
from models.schema import AgentSchema, JudgeSchema
from utils.database import DatabaseUtil
from langchain_core.messages import HumanMessage
from langchain_openai.chat_models.base import OpenAIConnectionError

llm = pick_llm("medium")
llm_judge = llm.with_structured_output(JudgeSchema)

sql_query = "DELETE * FROM users WHERE age > 30;"

prompt = f"""
You are an SQL Judge for data security. Your task is to determine whether the SQL query is
safe or not. The SQL query should only be used for data retrieval and should not modify the
database in any way. Neither the SQL query nor the prompt should contain any SQL commands that can modify the
database, such as INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, or any other commands that can change
the structure or content of the database. If the SQL query is safe, respond with 'Yes' otherwise respond with
'No'. Additionally, provide comments explaining your decision. 
Here's the SQL Query to evaluate : 
{sql_query} """

try:
	print(llm_judge.invoke(prompt))
except OpenAIConnectionError as error:
	raise RuntimeError(
		"Could not connect to OpenAI. Check your internet/DNS connection and "
		"OPENAI_API_KEY, then try again."
	) from error

response = llm_judge.invoke(prompt).model_dump()