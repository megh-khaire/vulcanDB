from collections import deque


def add_edge(graph, table, depends_on):
    graph[depends_on].append(table)


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


def get_query_execution_order(table_order, table_query_map):
    queries = []
    for table in table_order:
        queries.append(table_query_map[table])
    return queries
