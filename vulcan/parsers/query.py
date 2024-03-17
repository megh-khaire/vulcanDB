from mo_sql_parsing import parse


def extract_column_from_parsed_query(parsed_query):
    columns = []
    if "columns" in parsed_query:
        # Multiple Columns:
        if isinstance(parsed_query["columns"], list):
            for column in parsed_query["columns"]:
                if "name" in column:
                    columns.append(column["name"])
        # Single Column:
        else:
            column = parsed_query["column"]
            if "name" in column:
                columns.append(column["name"])
    return columns


def extract_constraints_from_parsed_query(parsed_query):
    foreign_keys = []
    if "constraint" in parsed_query:
        # Multiple Constraints:
        if isinstance(parsed_query["constraint"], list):
            for constraint in parsed_query["constraint"]:
                if "foreign_key" in constraint:
                    fk_table = constraint["foreign_key"]["references"]
                    foreign_keys.append(fk_table["table"])
        # Single Constraint:
        else:
            constraint = parsed_query["constraint"]
            if "foreign_key" in constraint:
                fk_table = constraint["foreign_key"]["references"]
                foreign_keys.append(fk_table["table"])
    return foreign_keys


def parse_sql_query(query: str):
    parsed_query = parse(query)["create table"]
    return {
        "query": query,
        "name": parsed_query["name"],
        "columns": extract_column_from_parsed_query(parsed_query),
        "foreign_keys": extract_constraints_from_parsed_query(parsed_query),
    }


def create_query_dependency_graph(queries: list):
    tables = {}
    dependency_graph = {}
    for query in queries:
        table_info = parse_sql_query(query)
        table_name = table_info["name"]
        tables[table_name] = table_info
        if table_name in dependency_graph:
            dependency_graph[table_name] + table_info["foreign_keys"]
        else:
            dependency_graph[table_name] = table_info["foreign_keys"]
    return dependency_graph, tables
