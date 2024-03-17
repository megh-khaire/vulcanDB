from mo_sql_parsing import parse


def parse_sql_query(query: str):
    parsed_query = parse(query)["create table"]
    table_name = parsed_query["name"]
    foreign_keys = []
    if "constraint" in parsed_query:
        for constraint in parsed_query["constraint"]:
            if "foreign_key" in constraint:
                fk_table = constraint["foreign_key"]["references"]
                foreign_keys.append(fk_table["table"])
    return table_name, foreign_keys


def create_query_dependency_graph(queries: list):
    table_query_map = {}
    dependency_graph = {}
    for query in queries:
        table_name, foreign_keys = parse_sql_query(query)
        table_query_map[table_name] = query
        if table_name in dependency_graph:
            dependency_graph[table_name] + foreign_keys
        else:
            dependency_graph[table_name] = foreign_keys
    return dependency_graph, table_query_map
