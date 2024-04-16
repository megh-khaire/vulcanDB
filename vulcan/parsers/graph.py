from collections import deque

from vulcan.parsers.query import parse_sql_query


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


def get_table_creation_order(graph):
    # Count of incoming edges for each vertex
    in_degree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1

    # Queue for vertices with no incoming edge
    queue = deque([u for u in in_degree if in_degree[u] == 0])

    # List to store the order of tables
    order = []

    while queue:
        vertex = queue.popleft()
        order.append(vertex)

        for neighbor in graph[vertex]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) == len(in_degree):
        return order
    else:
        raise Exception("Graph has at least one cycle, topological sort not possible.")
