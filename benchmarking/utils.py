import pandas as pd

STATS_FILE = "benchmarking/output/stats.csv"


def write_benchmarking_data(data):
    df = pd.DataFrame([data])
    with open(STATS_FILE, "a") as f:
        df.to_csv(f, header=f.tell() == 0, index=False)
