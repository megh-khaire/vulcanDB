from io import StringIO
from typing import Optional
import pandas as pd


def clean_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    # Remove unnamed columns
    dataframe = dataframe.loc[:, ~dataframe.columns.str.contains("^Unnamed")]
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


def get_dataframe_description(dataframe: pd.DataFrame):
    # Generate the description as before
    buffer = StringIO()
    dataframe.info(buf=buffer)
    info = buffer.getvalue()
    buffer.close()

    # Extract only the column information part
    lines = info.split("\n")
    column_info_lines = [
        line for line in lines if line.startswith(" ") or line.startswith("#")
    ]

    # Reformat to match the requested output
    output = "Column          Non-Null     Count       Dtype\n" + "\n".join(
        column_info_lines[1:]
    )
    return output


def get_dataframe_samples(dataframe: pd.DataFrame, sample_size: int = 10) -> str:
    """Return a string representation of a sample of the DataFrame.

    Parameters:
    - dataframe: The DataFrame to sample from.
    - sample_size: The number of samples to return.

    Returns:
    - A string representation of the DataFrame sample.
    """
    if not dataframe.empty:
        return dataframe.sample(n=min(sample_size, len(dataframe))).to_string()
    else:
        return "DataFrame is empty."
