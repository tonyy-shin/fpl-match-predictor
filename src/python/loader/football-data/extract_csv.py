import pandas as pd
import os
from pathlib import Path
import requests

url = "https://football-data.co.uk/mmz4281/"
start_year = 1993 # football-data.co.uk data starts from season 1993

def season_code(start_year: int) -> str:
    return f"{start_year % 100:02d}{(start_year + 1) % 100:02d}"


def extract_csv(url, output_path, start_year):
    while (
        requests.get(f"{url}{season_code(start_year)}/E0.csv", timeout=30).status_code == 200
        and
        requests.get(f"{url}{season_code(start_year)}/E1.csv", timeout=30).status_code == 200
        ):
        season = season_code(start_year)
        new_url_pl = f"{url}{season}/E0.csv"
        new_url_ch = f"{url}{season}/E1.csv"
        try:
            resp = requests.get(new_url_pl, timeout=30)
            resp.raise_for_status()
            if resp.content == b"":
                print(f"No content found for {new_url_pl}")
                continue
            out = Path(f"{output_path}/pl_{season}.csv")
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(resp.content)
            print(f"Downloaded premier league season {season} to {out}")
            start_year += 1
        except requests.RequestException as e:
            print(f"Failed to download {new_url_pl}: {e}")
        try:
            resp = requests.get(new_url_ch, timeout=30)
            resp.raise_for_status()
            if resp.content == b"":
                print(f"No content found for {new_url_ch}")
                continue
            out = Path(f"{output_path}/ch_{season}.csv")
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(resp.content)
            print(f"Downloaded championship season {season} to {out}")
        except requests.RequestException as e:
            print(f"Failed to download {new_url_ch}: {e}")



if __name__ == "__main__":
    extract_csv(url, "data/raw/football_data", start_year)