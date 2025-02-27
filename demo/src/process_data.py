import pandas as pd
import sys

def process_dataframe(path):
    df = pd.read_parquet(path, engine="pyarrow")
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])

    df["duration"] = (df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]).dt.total_seconds() / 60

    df = df[(df["duration"] >= 1) & (df["duration"] <= 60)]

    categorical = ["PULocationID", "DOLocationID"]
    df[categorical] = df[categorical].astype(str)

    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']

    df.to_parquet("pipelineOutput/processed/processed_data.parquet")
    return df

if __name__ == "__main__":
    path = sys.argv[1]  # Read input file path from command-line args
    df = process_dataframe(path)