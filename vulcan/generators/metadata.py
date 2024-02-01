from io import StringIO
import pandas as pd


def read_csv(csv_file_path: str):
    return pd.read_csv(csv_file_path)


def get_dataframe_description_modified(dataframe: pd.DataFrame):
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
    output = "Column          Non-Null     Count       Dtype\n" + "\n".join(column_info_lines[1:])
    return output


def get_dataframe_samples(dataframe: pd.DataFrame):
    df_samples = dataframe.sample(n=min(5, len(dataframe))).reset_index(drop=True)
    rows = []
    for index, sample in df_samples.iterrows():
        sample_text = ", ".join(f"{key}: {value}" for key, value in sample.items())
        rows.append(f"Row {index + 1}: {sample_text}")
    return "\n".join(rows)
