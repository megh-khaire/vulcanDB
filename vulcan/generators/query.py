import vulcan.generators.metadata as vgm
from vulcan.utils.hugging_face import llm_api


def generate_sql_queries(csv_file_path: str):
    df = vgm.read_csv(csv_file_path)
    info = vgm.get_dataframe_description(df)
    samples = vgm.get_dataframe_samples(df)
    prompt = f"""
As an expert database designer, you are tasked with creating a Postgres database schema from raw data. Your goal is to design a normalized schema that adheres to ACID properties. To assist in this task, detailed information about the data is provided below:

{info}

Additionally, here are some sample entries from the raw data file to give you insight into the data format:

{samples}

Based on this information, craft the SQL queries necessary to create the database schema. These queries should include the creation of tables, defining primary keys, setting up foreign keys for relationships, and ensuring normalization of the database. Specific details such as data types for each column and constraints should also be included.

Output the SQL queries that will help in constructing the table schema for this database.

Output:
"""
    return llm_api({"inputs": prompt})
