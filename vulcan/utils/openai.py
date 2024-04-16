import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def openai_chat_api(messages, **kwargs):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(messages=messages, **kwargs)
    return response.choices[0].message.content


def generate_schema(data: dict) -> dict:
    system_prompt = """
### Task ###
Create a relational database schema from the raw data and structure provided by the user.

### Instructions ###
1. Analyze the raw data and its structure provided by the user.
2. Define a relational schema that organizes this data into tables.
3. For each table, specify the columns, their data types, and relationships between tables.
4. Ignore unrelated or redundant columns while generating the schema.
5. Create multiple tables only when it is required.
6. Refrain from splitting schema into unecessary tables.
7. Refrain from directly generating SQL Queries.

### Input Data ###
1. raw_data: An example of the raw data that will be store in the schema.
2. structure: Information about the datatype for each column

## Desired Output ###
schema: A detailed relational schema including table names, column names with data types, and table relationships.
"""
    user_prompt = f"""
### Raw Data Sample ###
{data['raw_data']}


### Raw Data Structure ###
{data['structure']}


Output Schema:
"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    data["schema"] = openai_chat_api(messages, model="gpt-4-turbo", temperature=0.7)
    print(">> GENERATED SCHEMA ", data["schema"])
    return data


def generate_constraints(data: dict) -> dict:
    system_prompt = """
### Task ###
Identify constraints in the relational database schema provided by the user.

### Instructions ###
1. Examine the provided raw data and schema.
2. Identify all primary keys (PK) and foreign keys (FK) within the schema.
3. Determine any additional constraints that should be applied to ensure data integrity.
4. Create strict and detailed constraints.
5. Refrain from directly generating SQL Queries.

### Input Data ###
1. raw_data: An example of the raw data that will be store in the schema.
2. schema: A detailed relational schema including table names, column names with data types, and table relationships.

## Desired Output ###
constrainted schema: A relational schema consisting of all applicable constraints.
"""
    user_prompt = f"""
### Raw Data Sample ###
{data['raw_data']}


### Schema ###
{data["schema"]}


Constrained Schema:
"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    data["constrained_schema"] = openai_chat_api(
        messages, model="gpt-4-turbo", temperature=1
    )
    print(">> GENERATED CONSTRAINTS ", data["constrained_schema"])
    return data


def generate_sql_queries(data: dict) -> dict:
    system_prompt = """
### Task ###
Generate syntactically correct CREATE TABLE queries for the schema provided by the user.

### Instructions ###
1. Using the provided schema and constraints, generate CREATE TABLE statements for {database} database.
2. Ensure each table includes the necessary keys (primary and foreign) and specified constraints.
3. The queries should be syntactically correct to run on {database} database.
4. Return only the generated queries.
5. Refrain from returning any additional text apart from the queries.
6. Separate each query with double new lines.

### Input Data ###
schema: A relational schema consisting of all applicable constraints

## Desired Output ###
queries: CREATE TABLE statements for creating the given schema by incorporating all its constraints.
"""
    user_prompt = f"""
### Schema ###
{data["schema"]}


SQL Queries:
"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    data["queries"] = openai_chat_api(messages, model="gpt-4-turbo", temperature=0.7)
    print(">> GENERATED QUERIES ", data["queries"])
    return data
