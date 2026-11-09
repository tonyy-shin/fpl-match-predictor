import pandas as pd
import os
from pathlib import Path
import requests
from csv_to_parquet import csv_to_parquet
from extract_csv import extract_csv

url = "https://football-data.co.uk/mmz4281/"
csv_output_path = "data/raw/football_data"
parquet_output_path = "data/parquet/football_data"
start_year = 1993
end_year = 2027

if __name__ == "__main__":
    extract_csv(url, csv_output_path, start_year, end_year)
    csv_to_parquet(csv_output_path, parquet_output_path)