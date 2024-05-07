import os
import subprocess
import argparse
import time
import pandas as pd
from vulcan.testers.constraint import count_constraints


def append_dict_as_row(data):
    csv_output_file = 'benchmarking/output/stats.csv'
    df = pd.DataFrame([data])
    with open(csv_output_file, 'a') as f:
        df.to_csv(f, header=f.tell() == 0, index=False)


def generate_create_table_sql_to_file(csv_file_path, table_name, output_folder='output', dialect='sqlite'):
    """
    Generates a CREATE TABLE SQL command for a specified CSV file and writes it to a file in the specified folder.
    """
    try:
        start_time = time.time()
        # Ensure the output directory exists
        os.makedirs(output_folder, exist_ok=True)

        # Build the command to run csvsql
        command = ['csvsql', '--table', table_name,
                   '--dialect', dialect, csv_file_path]

        # File to write the SQL command
        file_path = os.path.join(
            output_folder, f"{table_name}_create_table.sql")

        # Execute the command and write to file
        with open(file_path, 'w') as file:
            result = subprocess.run(
                command, capture_output=True, text=True, check=True)
            if result.stdout:
                execution_time = time.time() - start_time
                stats = {}
                queries = result.stdout.split(';')[:-1]
                for query in queries:
                    query_constraints = count_constraints(query)
                    for key in set(stats) | set(query_constraints):
                        stats[key] = stats.get(
                            key, 0) + query_constraints.get(key, 0)
                no_of_queries = len(result.stdout.split(';')) - 1
                no_total_constraints = sum(stats.values())
                stats.update({
                    "dataset": os.path.basename(csv_file_path) + " csvkit",
                    "execution_time": execution_time,
                    "total_num_constraints": no_total_constraints,
                    "num_tables": no_of_queries,
                    # TODO: Implement get_missing_columns
                    "no_of_missing_columns": 0,
                    "masked": False
                })
                append_dict_as_row(stats)
                print(result.stdout)
                print(stats)

        print(f"SQL command written to: {file_path}")
        return file_path
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate SQL CREATE TABLE commands from a CSV file.")
    parser.add_argument('-c', '--csv', type=str,
                        required=True, help="Path to the CSV file")
    parser.add_argument('-t', '--table', type=str, required=True,
                        help="Name of the table to be created")
    parser.add_argument('-o', '--output', type=str,
                        default='output', help="Output folder for the SQL file")
    parser.add_argument('-d', '--dialect', type=str, default='sqlite', choices=[
                        'sqlite', 'postgresql', 'mysql'], help="SQL dialect for the CREATE TABLE command")

    args = parser.parse_args()

    generate_create_table_sql_to_file(
        args.csv, args.table, args.output, args.dialect)


if __name__ == "__main__":
    main()
