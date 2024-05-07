import argparse
import os
import subprocess
import time

from benchmarking.utils import write_benchmarking_data
from vulcan.testers.constraint import count_constraints


def generate_create_table_sql_to_file(csv_file_path, table_name, db_type):
    """
    Generates a CREATE TABLE SQL command for a specified CSV file and writes it to a file in the specified folder.
    """
    try:
        # Build the command to run csvsql
        command = ["csvsql", "--table", table_name, "--dialect", db_type, csv_file_path]

        start_time = time.time()
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        query = result.stdout
        execution_time = time.time() - start_time

        stats = count_constraints(query)
        stats.update(
            {
                "dataset": os.path.basename(csv_file_path),
                "tool": "csvkit",
                "execution_time": execution_time,
                "total_num_constraints": sum(stats.values()),
                "num_tables": 1,
                "no_of_missing_columns": 0,
                "masked": False,
            }
        )

        write_benchmarking_data(stats)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate SQL CREATE TABLE commands from a CSV file."
    )
    parser.add_argument(
        "-f", "--file_name", type=str, help="File name containing SQL queries"
    )
    parser.add_argument(
        "-t", "--table", type=str, required=True, help="Name of the table to be created"
    )
    parser.add_argument(
        "--db_type",
        type=str,
        choices=["postgres", "sqlite"],
        help="Type of the database",
        default="sqlite",
    )

    args = parser.parse_args()
    generate_create_table_sql_to_file(args.file_name, args.table, args.db_type)


if __name__ == "__main__":
    main()
