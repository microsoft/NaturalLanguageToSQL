import openai
import requests
import pyodbc
import re
import json
import urllib.request

# Define the database connection parameters
db_host="<your azure SQL Server name>"
server = 'tcp:' + db_host +'.database.windows.net;PORT=1433'
database = "<your azure SQL DB name>"
username = "<your azure SQL User name>"
password = "<your azure SQL Password>"

# Establish the database connection
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Define the endpoint URL and API key
endpoint_url = 'https://<your phi3 serverless deployment name>-serverless.eastus2.inference.ai.azure.com/chat/completions'
api_key = '<api key from serverless phi-3 deployment>'

# Define the headers for the request
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

# Define the payload with the natural language query
payload = {
    'messages': [
        { 
            'role': 'user', 
            'content': 'You are an AI assistant that helps users convert natural language to SQL queries. please follow these instructions. Given an input question, first create a syntactically correct SQL query to run, return only the query with no additional comments. Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the TOP clause as per SQL. Format the query for SQL using the following instructions: Never query for all columns from a table, you must query only the columns that are needed to answer the question. Never make a query using columns that do not exist, you must use only the column names you can see in the tables. Pay attention to use CURRENT_DATE to get the current date, if the question involves today. You should always generate a query based on the schema and the tables. If you cant find an answer return an a polite message. Ensure the query follows rules: No INSERT, UPDATE, DELETE, CREATE, ALTER, DROP instructions. Only SELECT queries for data retrieval. Dont add ```sql to the output SQL Query. Use the following exact format: SQLQuery: <SQL Query to run>. Return only the generated query without any additional comments. Only use the following Schema to identify tables and columns: CREATE TABLE [dbo].[Customers] ([CustomerID] INT NOT NULL, [CustomerName] VARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, [Email] VARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, CONSTRAINT [PK__Customer__A4AE64B84AB20F57] PRIMARY KEY ([CustomerID] ASC)). CREATE TABLE [dbo].[Orders] ([OrderID] INT NOT NULL, [CustomerID] INT NULL, [OrderDate] DATE NULL, [TotalAmount] DECIMAL(10,2) NULL, CONSTRAINT [PK__Orders__C3905BAFA5B4CF45] PRIMARY KEY ([OrderID] ASC)). Example Query: SELECT CustomerID, CustomerName, Email FROM Customers. Get total number of Orders for each Customer'
        }
    ],   
    'max_tokens': 1024,
    'temperature': 0,
    'top_p': 1
}


# Make the POST request to the endpoint
response = requests.post(endpoint_url, headers=headers, data=json.dumps(payload))
print(response)
if response.status_code == 200:
    # Parse the response JSON
    response_data = response.json()
    print(response_data)
    content = response_data['choices'][0]['message']['content']
    sql_query = content.replace('SQLQuery: ', '').strip().split(';')[0] + ';'.replace('"','')
    print("Generated SQL Query:")
    print(sql_query)


    # Establish the database connection
    # connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
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
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)