import argparse

from dotenv import load_dotenv

from vulcan.database.core import populate_database
from vulcan.generators.query import generate_sql_queries
from vulcan.parsers.graph import create_query_dependency_graph, get_table_creation_order
from vulcan.readers.csv import read_csv

load_dotenv()


def run_pipeline(file_name, db_uri, db_type):
    dataframe = read_csv(file_name)
    response = generate_sql_queries(dataframe, db_type)
    queries = response["queries"].split("\n\n")
    dependency_graph, tables = create_query_dependency_graph(queries)
    table_order = get_table_creation_order(dependency_graph)
    populate_database(db_uri, table_order, tables, dataframe)


def main():
    parser = argparse.ArgumentParser(description="Process some arguments.")
    parser.add_argument(
        "-f", "--file_name", type=str, help="File name containing SQL queries"
    )
    parser.add_argument(
        "--db_uri", type=str, help="Path to the database file", default=None
    )
    parser.add_argument(
        "--db_type",
        type=str,
        choices=["postgres", "sqlite"],
        help="Type of the database",
        default="sqlite",
    )

    args = parser.parse_args()
    file_name = args.file_name
    db_uri = args.db_uri
    db_type = args.db_type

    run_pipeline(file_name, db_uri, db_type)


if __name__ == "__main__":
    main()
