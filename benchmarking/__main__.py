import time
import argparse

from vulcan.app import run_pipeline
from vulcan.readers.csv import read_csv
from vulcan.testers.column import get_missing_columns
from vulcan.testers.constraint import count_constraints
from vulcan.app import run_pipeline


def run_benchmarking_pipeline(file_name, db_uri, db_type):
    start_time = time.time()
    dataframe = read_csv(file_name)
    response = run_pipeline(dataframe, db_uri, db_type)
    execution_time = time.time() - start_time
    total_constraints = 0
    for query in response["queries"]:
        total_constraints += sum(count_constraints(query).values())
    no_of_missing_columns = len(
        get_missing_columns(response["queries"], dataframe))
    no_of_queries = len(response["queries"])

    return {
        "execution_time": execution_time,
        "num_constraints": total_constraints,
        "num_tables": no_of_queries,
        "no_of_missing_columns": no_of_missing_columns,
    }


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

    results = run_benchmarking_pipeline(file_name, db_uri, db_type)
    for key, value in results.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
