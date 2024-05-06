import argparse

from vulcan.app import run_pipeline
from vulcan.readers.csv import read_csv


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

    dataframe = read_csv(file_name)
    run_pipeline(dataframe, db_uri, db_type)


if __name__ == "__main__":
    main()
