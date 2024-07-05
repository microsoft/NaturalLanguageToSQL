# Natural Language (NL) to SQL Query Generation using Phi-3 (Serverless & Local setup) and Azure OpenAI (GPT-4 model) 

This repo contains 3 variations of processing Natural Language (NL) to SQL Query.

## 1. Phi-3 Serverless

This project [NLToSql-Phi3_ServerlessDeployment.py](NLToSql-Phi3_ServerlessDeployment.py) demonstrates how to use the Phi-3 model deployed as a serverless API in Azure to convert natural language queries to SQL queries. The project includes Python code to call the Phi-3 serverless chat completion endpoint, extract the generated SQL query, Query the SQL Database and handle various response scenarios.

[Deploy Phi-3 family of small language models with Azure AI Studio](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/deploy-models-phi-3?tabs=phi-3-medium)

Model: Phi-3-mini-128k-Instruct

## 2. Phi-3 on Local Ollama

This project [ NLPToSQL-phi3_local.py](NLToSql-phi3_local.py)demonstrates how to use the Phi-3 model deployed in local laptop (Ollama) to convert natural language queries to SQL queries.

### Requirements
```
Install Ollama - https://ollama.com/ 
ollama pull phi3
ollama run phi3
```

## 3. NL to SQL Queries using LangChain and GPT-4

This project [NLToSql_GPT4.py](NLToSql_GPT4.py) is standard way to generate SQL queries with GPT4.
[Deploy GPT4 from Azure OpenAI Studio](https://learn.microsoft.com/en-us/azure/ai-services/openai/chatgpt-quickstart?tabs=command-line%2Cpython-new&pivots=programming-language-studio)


### Local Run

To run locally:

```
python -m venv <directory>
venv\Scripts\activate
Install Dependencies - pip install langchain_openai openai pyodbc fastapi uvicorn[standard] pydantic azure-identity langchain_community
python .\NLToSql-Phi3_ServerlessDeployment.py (or) python .\NLToSql-phi3_local.py (or) python .\NLToSql_GPT4.py
```

### DB Schemas:
CREATE TABLE [dbo].[Customers] ([CustomerID] INT NOT NULL, [CustomerName] VARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, [Email] VARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, CONSTRAINT PRIMARY KEY ([CustomerID] ASC)). 
CREATE TABLE [dbo].[Orders] ([OrderID] INT NOT NULL, [CustomerID] INT NULL, [OrderDate] DATE NULL, [TotalAmount] DECIMAL(10,2) NULL, CONSTRAINT PRIMARY KEY ([OrderID] ASC))


## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

