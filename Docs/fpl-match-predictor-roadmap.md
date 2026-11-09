# FPL Match Predictor — Project Roadmap

**Goal:** Predict Premier League match outcomes (home win / draw / away win probabilities), built first as a data engineering project and then as a data science / ML project.

**Success metric:** Log loss or Brier score, benchmarked against bookmaker implied odds.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Ingestion | Python (requests, pandas, pyarrow) |
| Raw storage | Parquet files (unchanged API responses) |
| Warehouse | PostgreSQL (in Docker) |
| Transformation & testing | dbt Core (`pip install dbt-postgres`) |
| Orchestration | Apache Airflow (via Astro CLI); cron / GitHub Actions to start |
| ML | scikit-learn, LightGBM, Poisson / Dixon-Coles |
| Experiment tracking | MLflow |
| Dashboard | Streamlit |

---

## Roadmap

### 1. Define target & pick data sources
- Target: match result (W/D/L) probabilities
- Sources:
  - **football-data.co.uk** — historical results + bookmaker odds (CSV, many seasons)
  - **FPL API** — current-season fixtures, team strength, injuries
  - **Understat** — xG data (scraped)

### 2. Ingest raw data to Parquet (Python)
- Save full, unmodified responses — don't filter yet
- Feature selection happens later in dbt
- Partition files by source and date

### 3. Load into Postgres
- Load Parquet into a `raw` schema
- Make loads **incremental and idempotent** (re-running produces the same result, no duplicates)

### 4. Transform + test with dbt
- Layers: `staging` → `intermediate` → `marts`
  - `stg_*` — rename columns, cast types
  - `int_*` — joins, rolling form, Elo
  - `mart_match_features` — one row per match, ML-ready
- Tests written alongside each model: `unique`, `not_null`, `accepted_values`, relationships
- Watch out: team name mapping across sources ("Man Utd" vs "Manchester United")
- Run everything with `dbt build`

### 5. Quick baseline model (sanity check)
- Fit Elo or logistic regression on form features
- Compare against bookmaker odds
- Confirms the data is useful before investing in orchestration

### 6. Schedule with Airflow
- Get the pipeline working end-to-end as plain scripts first
- DAG: `check_gameweek_finished → extract → load → dbt_build → predict`
- Run daily; `ShortCircuitOperator` skips if the gameweek isn't finished (FPL API `finished` / `data_checked` flags)
- Use Astro CLI (`astro dev start`) for local setup
- Optional: Cosmos to render dbt models as Airflow tasks

### 7. Full ML model (longest phase)
- EDA: home advantage, draw rates, xG vs goals
- Features: rolling form, xG for/against, Elo, rest days, injuries
- **Point-in-time correctness** — features use only data available before kickoff (no leakage)
- Models: Poisson / Dixon-Coles → LightGBM
- Time-based train/test splits (by season), never random
- Check probability calibration
- Track experiments in MLflow

### 8. Serve & monitor
- Write weekly predictions back to Postgres
- Streamlit dashboard: predictions vs. actual results vs. bookmaker odds
- Track live performance through the season; retrain on a schedule

---

## Stretch Goals
- Port the warehouse to BigQuery (free sandbox) or Snowflake
- Run the pipeline in the cloud (GitHub Actions + hosted Postgres like Neon/Supabase)
- Extend to scoreline prediction

## Learning Resources
- dbt Fundamentals (free): learn.getdbt.com
- Airflow official docs (match the version Astro installs)
