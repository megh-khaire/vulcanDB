import os
import time
import argparse
import pandas as pd

from vulcan.app import run_pipeline
from vulcan.testers.column import get_missing_columns
from vulcan.testers.constraint import count_constraints
from vulcan.app import run_pipeline


def mask_column_names(dataframe):
    """Replace column names with masked names like 'Column1', 'Column2', etc."""
    new_columns = [f"Column{i+1}" for i in range(len(dataframe.columns))]
    return dataframe.rename(columns=dict(zip(dataframe.columns, new_columns)))


def append_dict_as_row(data):
    csv_output_file = 'benchmarking/output/stats.csv'
    df = pd.DataFrame([data])
    with open(csv_output_file, 'a') as f:
        df.to_csv(f, header=f.tell() == 0, index=False)


def run_benchmarking_pipeline_with_masking(file_name, db_uri, db_type):
    start_time = time.time()
    dataframe = pd.read_csv(file_name)

    # Mask column names in the dataframe
    masked_dataframe = mask_column_names(dataframe)

    response = run_pipeline(masked_dataframe, db_uri, db_type)
    execution_time = time.time() - start_time

    stats = {}
    for query in response["queries"]:
        query_constraints = count_constraints(query)
        for key in set(stats) | set(query_constraints):
            stats[key] = stats.get(key, 0) + query_constraints.get(key, 0)

    no_of_queries = len(response["queries"])
    no_of_missing_columns = len(get_missing_columns(
        response["queries"], masked_dataframe))
    no_total_constraints = sum(stats.values())

    stats.update({
        "dataset": os.path.basename(file_name) + " (masked)",
        "execution_time": execution_time,
        "total_num_constraints": no_total_constraints,
        "num_tables": no_of_queries,
        "no_of_missing_columns": no_of_missing_columns,
        "masked": True
    })

    append_dict_as_row(stats)
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
    file_name = args.file_name
    db_uri = args.db_uri
    db_type = args.db_type

    run_benchmarking_pipeline_with_masking(file_name, db_uri, db_type)


if __name__ == "__main__":
    main()
