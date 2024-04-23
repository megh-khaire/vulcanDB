from mo_sql_parsing import parse

import vulcan.parsers.query as vpq


def get_column_constraints(parsed_query, constraint_count):
    parsed_columns = vpq.extract_columns_from_parsed_query(parsed_query)
    for column in parsed_columns:
        if isinstance(column, dict):
            # Check for primary key, unique, not null, and default within column definition
            if "primary_key" in column:
                constraint_count["primary_key"] += 1
            if "nullable" in column:
                constraint_count["not_null"] += 1
            if "unique" in column:
                constraint_count["unique"] += 1
            if "default" in column:
                constraint_count["default"] += 1
            if column.get("check"):
                constraint_count["check"] += 1
    return constraint_count


def get_table_constraints(parsed_query, constraint_count):
    parsed_constraints = vpq.extract_table_constraints_from_parsed_query(parsed_query)
    for constraint in parsed_constraints:
        # Identify foreign key and check constraints
        if isinstance(constraint, dict):
            if constraint.get("foreign_key"):
                constraint_count["foreign_key"] += 1
            if constraint.get("check"):
                constraint_count["check"] += 1
    return constraint_count


def count_constraints(sql_query):
    # Initialize the counter for constraints
    constraint_count = {
        "primary_key": 0,
        "foreign_key": 0,
        "unique": 0,
        "check": 0,
        "not_null": 0,
        "default": 0,
    }

    # Parse the SQL query into a JSON structure
    parsed_query = parse(sql_query)["create table"]
    # Process column level constraints:
    constraint_count = get_column_constraints(parsed_query, constraint_count)
    # Process table level constraints:
    constraint_count = get_table_constraints(parsed_query, constraint_count)
    return constraint_count
