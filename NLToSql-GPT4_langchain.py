# Get LLM
import os
# from pathlib import Path
import re
from langchain.memory import ConversationBufferMemory
from langchain.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableParallel
from langchain_openai import AzureChatOpenAI
from langchain.chat_models import AzureChatOpenAI
from sqlalchemy import create_engine
from langchain.prompts.chat import ChatPromptTemplate

from langchain.agents import AgentType, create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

import urllib
import pyodbc, struct
from azure import identity
from typing import Union



db_host="<your azure SQL Server name>"
db_name="<your azure SQL DB name>"
db_user="<your azure SQL User name>"
db_password="<your azure SQL Password>"

os.environ["OPENAI_API_TYPE"]="azure"
os.environ["OPENAI_API_VERSION"]="2023-07-01-preview"
os.environ["OPENAI_API_BASE"]="<Your Azure OpenAI resource endpoint>"
os.environ["OPENAI_API_KEY"]="<Your Azure OpenAI resource key>"
os.environ["OPENAI_CHAT_MODEL"]="<Use name of deployment>"

driver = '{ODBC Driver 17 for SQL Server}'

driver = '{ODBC Driver 17 for SQL Server}'
odbc_str = 'mssql+pyodbc:///?odbc_connect=' \
                'Driver='+driver+ \
                ';Server=tcp:' + db_host +'.database.windows.net;PORT=1433' + \
                ';DATABASE=' + db_name + \
                ';Uid=' + db_user + \
                ';Pwd=' + db_password + \
                ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
db_engine = create_engine(odbc_str)

print('connection is ok')


llm = AzureChatOpenAI(model=os.getenv("OPENAI_CHAT_MODEL"),
                      deployment_name=os.getenv("OPENAI_CHAT_MODEL"),
                      temperature=0)

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", 
         """
          You are a helpful AI assistant expert in querying SQL Database to find answers to user's question.
         """
         ),
        ("user", "{question}\n ai: "),
    ]
)


db = SQLDatabase(db_engine)

sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
sql_toolkit.get_tools()

sqldb_agent = create_sql_agent(
    llm=llm,
    toolkit=sql_toolkit,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

sqldb_agent.run(final_prompt.format(
        question="Give me the total number of Orders?"
  ))