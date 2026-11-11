from pathlib import Path
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timezone
from src.python.loader.football_data.csv_to_parquet import csv_to_parquet
from src.python.loader.football_data.extract_csv import extract_csv


load_dotenv(find_dotenv())
connection_string = os.getenv("DATABASE_URL")
engine = create_engine(connection_string)
url = "https://football-data.co.uk/mmz4281/"
csv_file_path = "data/raw/football_data"
parquet_file_path = "data/parquet/football_data"
start_year = 1993 # football-data.co.uk data starts from season 1993


def insert_data(conn):
    loaded_at = datetime.now(timezone.utc)
    folder = Path(parquet_file_path)
    for path in sorted(folder.glob("*.parquet")):
        table_name = path.stem.lower()
        try:
            df = pd.read_parquet(path)
        except Exception as e:
            print(f"Error reading Parquet from {path}: {e}")
            continue
        df["loaded_at"] = loaded_at
        try:
            with conn.begin():
                df.to_sql(table_name, conn, if_exists="replace", index=False)
                print(f"Inserted data from {path} into table {table_name}")
        except SQLAlchemyError as e:
            print(f"Error inserting data from {path}: {e}")

if __name__ == "__main__":
    extract_csv(url, csv_file_path, start_year)
    csv_to_parquet(csv_file_path, parquet_file_path)
    with engine.connect() as conn:
        insert_data(conn)