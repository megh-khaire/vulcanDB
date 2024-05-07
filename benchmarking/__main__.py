import argparse
import os
import time

from benchmarking.utils import write_benchmarking_data
from vulcan.app import run_pipeline
from vulcan.readers.csv import read_csv
from vulcan.testers.column import get_missing_columns
from vulcan.testers.constraint import count_constraints


def run_benchmarking_pipeline(file_name, db_uri, db_type):
    start_time = time.time()
    dataframe = read_csv(file_name)
    response = run_pipeline(dataframe, db_uri, db_type)
    execution_time = time.time() - start_time

    stats = {}
    for query in response["queries"]:
        query_constraints = count_constraints(query)
        for key in set(stats) | set(query_constraints):
            stats[key] = stats.get(key, 0) + query_constraints.get(key, 0)

    no_of_queries = len(response["queries"])
    no_of_missing_columns = len(get_missing_columns(response["queries"], dataframe))
    no_total_constraints = sum(stats.values())

    stats.update(
        {
            "dataset": os.path.basename(file_name),
            "tool": "gpt-4-turbo",
            "execution_time": execution_time,
            "total_num_constraints": no_total_constraints,
            "num_tables": no_of_queries,
            "no_of_missing_columns": no_of_missing_columns,
            "masked": False,
        }
    )

    write_benchmarking_data(stats)
    return stats


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
    run_benchmarking_pipeline(args.file_name, args.db_uri, args.db_type)


if __name__ == "__main__":
    main()
