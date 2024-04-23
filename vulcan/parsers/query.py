from mo_sql_parsing import parse


def extract_columns_from_parsed_query(parsed_query):
    if "columns" in parsed_query:
        if isinstance(parsed_query["columns"], list):
            return parsed_query["columns"]
        return [parsed_query["columns"]]
    return []


def extract_table_constraints_from_parsed_query(parsed_query):
    if "constraint" in parsed_query:
        if isinstance(parsed_query["constraint"], list):
            return parsed_query["constraint"]
        return [parsed_query["constraint"]]
    return []


def extract_column_names_from_parsed_query(parsed_query):
    parsed_columns = extract_columns_from_parsed_query(parsed_query)

    columns = []
    for column in parsed_columns:
        if "name" in column:
            columns.append(column["name"])
    return columns


def extract_foreign_keys_from_parsed_query(parsed_query):
    table_constraints = extract_table_constraints_from_parsed_query(parsed_query)
    foreign_keys = []
    for constraint in table_constraints:
        if "foreign_key" in constraint:
            fk_table = constraint["foreign_key"]["references"]
            foreign_keys.append(fk_table["table"])
    return foreign_keys


def parse_sql_query(query: str):
    parsed_query = parse(query)["create table"]
    return {
        "query": query,
        "name": parsed_query["name"],
        "columns": extract_column_names_from_parsed_query(parsed_query),
        "foreign_keys": extract_foreign_keys_from_parsed_query(parsed_query),
    }
