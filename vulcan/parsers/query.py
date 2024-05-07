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


def extract_references_from_columns(parsed_query):
    foreign_tables = []
    parsed_columns = extract_columns_from_parsed_query(parsed_query)
    for column in parsed_columns:
        if "references" in column:
            foreign_tables.append(column["references"]["table"])
    return foreign_tables


def extract_references_from_table(parsed_query):
    table_constraints = extract_table_constraints_from_parsed_query(parsed_query)
    foreign_tables = []
    for constraint in table_constraints:
        if "foreign_key" in constraint:
            fk_table = constraint["foreign_key"]["references"]
            foreign_tables.append(fk_table["table"])
    return foreign_tables


def extract_foreign_keys_from_parsed_query(parsed_query):
    column_references = extract_references_from_columns(parsed_query)
    table_references = extract_references_from_table(parsed_query)
    return list(set(column_references + table_references))


def parse_sql_query(query: str):
    parsed_query = parse(query)["create table"]
    return {
        "query": query,
        "name": parsed_query["name"],
        "columns": extract_column_names_from_parsed_query(parsed_query),
        "foreign_keys": extract_foreign_keys_from_parsed_query(parsed_query),
    }
