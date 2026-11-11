import csv
import io
from pathlib import Path

import pandas as pd

csv_file_path = "data/raw/football_data"
parquet_file_path = "data/parquet/football_data"


def decode(raw: bytes, name: str) -> str:
    try:
        return raw.decode("utf-8-sig")  # also strips a BOM if present
    except UnicodeDecodeError as e:
        print(f"  {name}: byte {e.object[e.start]:#04x} at offset {e.start} "
              "is not UTF-8, falling back to latin-1")
        return raw.decode("latin-1")


def _read_raw_csv(path: Path) -> pd.DataFrame:
    text = decode(path.read_bytes(), path.name)
    rows = list(csv.reader(io.StringIO(text, newline="")))
    header = rows[0]
    width = max(len(r) for r in rows)
    columns = [h.strip() or f"_extra_{i}" for i, h in enumerate(header)]
    columns += [f"_extra_{i}" for i in range(len(header), width)]

    df = pd.read_csv(
        io.StringIO(text, newline=""),
        header=None,
        skiprows=1,
        names=columns,
        dtype=str,
        keep_default_na=False,
        na_values=[""],
        skip_blank_lines=False,
    )
    return df.dropna(axis=0, how="all").dropna(axis=1, how="all").reset_index(drop=True)


def csv_to_parquet(csv_file_path, parquet_file_path):
    out_dir = Path(parquet_file_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    for path in sorted(Path(csv_file_path).iterdir()):
        if path.suffix != ".csv":
            print(f"Skipping non-CSV file: {path.name}")
            continue
        df = _read_raw_csv(path)
        out = out_dir / f"{path.stem}.parquet"
        df.to_parquet(out, index=False)
        print(f"  wrote {out} ({len(df)} rows, {df.shape[1]} columns)")
    return parquet_file_path


if __name__ == "__main__":
    csv_to_parquet(csv_file_path, parquet_file_path)