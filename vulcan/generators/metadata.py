from io import StringIO
import pandas as pd


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
