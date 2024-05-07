from dotenv import load_dotenv

from vulcan.database.core import populate_database
from vulcan.generators.query import generate_sql_queries
from vulcan.parsers.graph import create_query_dependency_graph, get_table_creation_order

load_dotenv()


def run_pipeline(dataframe, db_uri, db_type):
    response = generate_sql_queries(dataframe, db_type)
    dependency_graph, tables = create_query_dependency_graph(
        response["queries"])
    table_order = get_table_creation_order(dependency_graph)
    populate_database(db_uri, table_order, tables, dataframe)
    return response
