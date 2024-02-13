from io import StringIO
import pandas as pd


def clean_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    # Removing unnamed columns
    dataframe = dataframe.loc[:, ~dataframe.columns.str.contains('^Unnamed')]
    # Remove rows with NaN values and assign the result back to dataframe
    dataframe = dataframe.dropna()
    return dataframe


def read_csv(csv_file_path: str):
    dataframe = pd.read_csv(csv_file_path)
    return clean_dataframe(dataframe)


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


def get_dataframe_samples(dataframe: pd.DataFrame):
    return dataframe.sample(n=10).to_string()
