import pandas as pd
import os
csv_file_path = "data/raw"
parquet_file_path = "data/parquet"

def csv_to_parquet(csv_file_path, parquet_file_path):
    for p in os.listdir(csv_file_path):
        if p.endswith(".csv"):
            df = pd.read_csv(os.path.join(csv_file_path, p))
            df.to_parquet(os.path.join(parquet_file_path, p.replace(".csv", ".parquet")), index=False)
        else:
            print(f"Skipping non-CSV file: {p}")
    return parquet_file_path

if __name__ == "__main__":
    output_path = csv_to_parquet(csv_file_path, parquet_file_path)
    print(f"Parquet files saved to: {output_path}")