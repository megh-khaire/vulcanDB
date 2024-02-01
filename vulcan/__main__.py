import argparse

from dotenv import load_dotenv

from vulcan.generators.query import generate_sql_queries

load_dotenv()


def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Process some arguments.")

    # Add arguments
    parser.add_argument("-f", type=str, help="File name")

    # Parse arguments
    args = parser.parse_args()

    # Access the arguments
    file_name = args.f

    print(generate_sql_queries(file_name))


if __name__ == "__main__":
    main()
