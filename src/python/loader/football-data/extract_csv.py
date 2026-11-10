import pandas as pd
import os
from pathlib import Path
import requests

url = "https://football-data.co.uk/mmz4281/"
start_year = 1993
end_year = 2027

def season_code(start_year: int) -> str:
    return f"{start_year % 100:02d}{(start_year + 1) % 100:02d}"

def extract_csv(url, output_path, start_year, end_year):
    for start in range(start_year, end_year):
        season = season_code(start)
        new_url = f"{url}{season}/E0.csv"
        try:
            resp = requests.get(new_url, timeout=30)
            resp.raise_for_status()
            if resp.content == b"":
                print(f"No content found for {new_url}")
                continue
            out = Path(f"{output_path}/pl_{season}.csv")
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(resp.content)
            print(f"Downloaded season {season} to {out}")
        except requests.RequestException as e:
            print(f"Failed to download {new_url}: {e}")
    for start in range(start_year, end_year):
            season = season_code(start)
            new_url = f"{url}{season}/E1.csv"
            try:
                resp = requests.get(new_url, timeout=30)
                resp.raise_for_status()
                if resp.content == b"":
                    print(f"No content found for {new_url}")
                    continue
                out = Path(f"{output_path}/ch_{season}.csv")
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(resp.content)
                print(f"Downloaded season {season} to {out}")
            except requests.RequestException as e:
                print(f"Failed to download {new_url}: {e}")


if __name__ == "__main__":
    extract_csv(url, "data/raw/football_data", start_year, end_year)