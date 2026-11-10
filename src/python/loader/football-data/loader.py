import pandas as pd
from pathlib import Path
import psycopg2
from config import load_config

conn = psycopg2.connect(**load_config())
conn.autocommit = True
c = conn.cursor()


create_table = """
CREATE TABLE IF NOT EXISTS football_data (
    id SERIAL PRIMARY KEY,
    team_name TEXT NOT NULL,
    league TEXT NOT NULL,
    points INT NOT NULL
)
"""