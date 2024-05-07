from io import StringIO

import pandas as pd


def get_dataframe_description(dataframe: pd.DataFrame) -> str:
    """
    Generates a formatted string describing the DataFrame's columns, non-null values, and data types.

    Parameters:
    - dataframe: The DataFrame to describe.

    Returns:
    - A formatted string with the description of DataFrame.
    """
    # Capture the DataFrame info in a string buffer
    buffer = StringIO()
    dataframe.info(buf=buffer)
    info = buffer.getvalue()
    buffer.close()

    # Extract and format the column information
    lines = info.split("\n")
    column_info_lines = [line for line in lines if line.strip()]
    # Prepare the formatted output
    formatted_output = "Column             Non-Null             Dtype\n"
    formatted_output += "-" * 40 + "\n"
    for line in column_info_lines[4:]:
        try:
            parts = line.strip().split()
            column_name = parts[1]
            non_null_count = parts[3]
            dtype = parts[4]
            formatted_output += f"{column_name:20} {non_null_count:15} {dtype}\n"
        except IndexError as _e:
            continue
    return formatted_output


def get_dataframe_samples(dataframe: pd.DataFrame, sample_size: int = 10) -> str:
    """
    Returns a string representation of a sample from the DataFrame.

    Parameters:
    - dataframe: The DataFrame to sample from.
    - sample_size: The number of samples to return.

    Returns:
    - A string representation of the DataFrame sample.
    """
    if not dataframe.empty:
        # Ensure the sample size does not exceed the number of available rows
        sample = dataframe.sample(n=min(sample_size, len(dataframe)))
        # Return a string representation of the sample without the index
        return sample.to_string(index=False)
    else:
        return "DataFrame is empty."
