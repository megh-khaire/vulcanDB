query_generation_prompt = [
    {
        "text": """Given some raw data and its structure, define a relational schema that includes tables, columns, and data types.

Raw data:
{raw_data}

Structure:
{structure}
""",
        "input_variables": ["raw_data", "structure"],
        "output_variable": "schema",
    },
    {
        "text": """Given schema for a relational database, identify primary keys, foreign keys, and any other constraints for the defined schema. Be as strict as possible!

Schema:
{schema}
""",
        "input_variables": ["schema"],
        "output_variable": "constraints",
    },
    {
        "text": """Generate only SQL CREATE TABLE queries based on the defined schema including keys and constraints.

Schema:
{schema}

Constraints:
{constraints}
        """,
        "input_variables": ["schema", "constraints"],
        "output_variable": "queries",
    },
]
