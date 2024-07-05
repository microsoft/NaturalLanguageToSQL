import openai
import pyodbc
import re

client = openai.OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="nokeyneeded",
)


db_host="<your azure SQL Server name>"
server = 'tcp:' + db_host +'.database.windows.net;PORT=1433'
database = "<your azure SQL DB name>"
username = "<your azure SQL User name>"
password = "<your azure SQL Password>"

SQLql_template = """
You are a SQL expert, please follow these instructions.
Given an input question, first create a syntactically correct SQL query to run, return only the query with no additional comments.
Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the TOP clause as per SQL.
Format the query for SQL using the following instructions:
Never query for all columns from a table, you must query only the columns that are needed to answer the question.
Never make a query using columns that do not exist, you must use only the column names you can see in the tables.
Pay attention to use CURRENT_DATE function to get the current date, if the question involves 'today'.
You should always try to generate a query based on the schema and the tables.
You should always try to generate an answer for all queries.
If you can't find an answer return an a polite message.
Ensure the query follows rules:
No INSERT, UPDATE, DELETE instructions.
No CREATE, ALTER, DROP instructions are.
Only SELECT queries for data retrieval. Don't include double quotes " to the queries. Don't add ```sql to the output.
Use the following exact format:
SQLQuery: <SQL Query to run>
Return only the generated query without any additional comments
Only use the following tables and columns:
CREATE TABLE [dbo].[Customers] ([CustomerID] INT NOT NULL, [CustomerName] VARCHAR(255), [Email] VARCHAR(255), CONSTRAINT PRIMARY KEY ([CustomerID] ASC)). 
CREATE TABLE [dbo].[Orders] ([OrderID] INT NOT NULL, [CustomerID] INT NULL, [OrderDate] DATE NULL, [TotalAmount] DECIMAL(10,2) NULL, CONSTRAINT PRIMARY KEY ([OrderID] ASC))
Example Query:
SELECT CustomerID, CustomerName, Email FROM Customers
""" 
response = client.chat.completions.create(
    model="phi3",
    temperature=0,
    n=1,
    messages=[
        {"role": "system", "content": SQLql_template},
        {"role": "user", "content": "Get total number of Orders for each Customer"},
    ],
)

print(response)
content = response.choices[0].message.content
print(content)
sql_query = content.replace('SQLQuery: ', '').strip().split(';')[0] + ';'.replace('"','')
print(sql_query)


# Establish the database connection
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Execute the generated SQL query
cursor.execute(sql_query)

# Fetch and print the results
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the database connection
cursor.close()
conn.close()

