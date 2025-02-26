import pandas as pd
import sys

def read_dataframe(path):
    df = pd.read_parquet(path, engine="pyarrow")
    df.to_parquet("data2/processed/read_data.parquet")
    return df

if __name__ == "__main__":
    path = sys.argv[1]  # Read input file path from command-line args
    df = read_dataframe(path)