import re
from typing import Optional

import pandas as pd


def convert_to_snake_case(column_names):
    """
    Converts a list of column names from camel case or space-separated to snake case.

    Parameters:
    - column_names: A list of strings representing the column names to be converted.

    Returns:
    - A list of strings with the column names converted to snake case.
    """
    snake_case_columns = []
    for name in column_names:
        cleaned_name = re.sub(r"\s*\([^)]*\)", "", name)
        name_with_underscores = cleaned_name.replace(" ", "_")
        snake_case = re.sub(r"(?<!^)(?=[A-Z])", "_", name_with_underscores).lower()
        snake_case_columns.append(snake_case)
    return snake_case_columns


def clean_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    # Remove unnamed columns
    dataframe = dataframe.loc[:, ~dataframe.columns.str.contains("^Unnamed")]
    dataframe.columns = convert_to_snake_case(dataframe.columns)
    # Remove rows with NaN values and assign the result back to dataframe
    dataframe = dataframe.dropna()
    return dataframe


def read_csv(csv_file_path: str, fillna: Optional[dict] = None) -> pd.DataFrame:
    """Read a CSV file into a DataFrame, clean it, and optionally fill NaN values.

    Parameters:
    - csv_file_path: Path to the CSV file.
    - fillna: Dictionary specifying values to fill NaNs for specific columns, e.g., {'column_name': 0}.

    Returns:
    - A cleaned DataFrame.
    """
    try:
        dataframe = pd.read_csv(csv_file_path)
        dataframe = clean_dataframe(dataframe)
        if fillna is not None:
            dataframe.fillna(value=fillna, inplace=True)
        return dataframe
    except FileNotFoundError:
        print(f"Error: File {csv_file_path} not found.")
    except pd.errors.EmptyDataError:
        print("Error: No data in CSV file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
