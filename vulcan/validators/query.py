import sqlvalidator
from sqleyes.main import main as sqleyes_main


def find_sql_anti_patterns(query: str):
    anti_patterns = sqleyes_main(query)
    return anti_patterns


def validate_sql_query(query: str):
    # Parsing the sql query
    parsed_query = sqlvalidator.parse(query)
    # Check the validity of the parsed query
    is_valid = parsed_query.is_valid()
    # Return the validity and errors if any
    return is_valid, parsed_query.errors


def validate_all_sql_queries(queries: list):
    processed_queries = []
    for query in queries:
        query = query.strip()
        is_valid, error = validate_sql_query(query)
        if is_valid:
            processed_queries.append(query)
    return processed_queries
