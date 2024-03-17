query_generation_prompt = [
    {
        "text": """
        Task: Create a relational database schema from provided raw data.

        Instructions:
        1. Analyze the raw data and its structure provided below.
        2. Define a relational schema that organizes this data into tables.
        3. For each table, specify the columns, their data types, and relationships between tables if applicable.
        4. Ignore unrelated or redundant columns while generating the schema

        Input Variables:
        - raw_data: A description or example of the raw data to be organized.
        - structure: Information about the structure or format of the raw data.

        Desired Output:
        - schema: A detailed relational schema including table names, column names with data types, and table relationships.

        ========================================
        raw_data:

        {raw_data}
        ========================================
        structure:

        {structure}
        ========================================
        Output Schema:
        """,
        "input_variables": ["raw_data", "structure"],
        "output_variable": "schema",
    },
    {
        "text": """
        Task: Identify keys and all possible constraints in a relational database schema.

        Instructions:
        1. Examine the provided schema for a relational database.
        2. Identify all primary keys (PK) and foreign keys (FK) within the schema.
        3. Determine any additional constraints (e.g., unique, not null, etc) that should be applied to ensure data integrity.
        4. Be as detailed and strict as possible in specifying these constraints.

        Input Variable:
        - schema: The schema of the relational database, including table and column definitions.

        Desired Output:
        - constraints: A comprehensive list of all keys (PK and FK) and constraints for the schema, specifying which table and column they apply to.

        ========================================
        schema:

        {schema}
        ========================================
        Output Constraints:
        """,
        "input_variables": ["schema"],
        "output_variable": "constraints",
    },
    {
        "text": """
        Task: Generate SQL CREATE TABLE queries from a schema with constraints.

        Instructions:
        1. Using the provided schema and constraints, generate SQL CREATE TABLE statements for {database}.
        2. Ensure each statement includes the necessary keys (primary and foreign) and any other specified constraints.
        3. The queries should be ready to execute in a SQL database, properly formatting SQL syntax.
        4. Return only the generated queries, no additional text is required.

        Input Variables:
        - schema: The schema definitions for the tables including column names and types.
        - constraints: The constraints identified for the schema, including primary keys, foreign keys, and others.

        Desired Output:
        - queries: A set of SQL CREATE TABLE statements that reflect the schema and incorporate all constraints.

        ========================================
        schema:

        {schema}
        ========================================
        constraints:

        {constraints}
        ========================================
        Output Queries:
        """,
        "input_variables": ["schema", "constraints", "database"],
        "output_variable": "queries",
    },
]
