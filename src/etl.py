# src/etl.py
# ------------------------------------------------------------
# SIMPLE ETL: read one day's CSV, compute session minutes,
# aggregate per player, and load to SQLite fact table.
#
# Usage:
#   python src/etl.py 2025-09-18
# Airflow will call main(for_date) with {{ ds }}.
# ------------------------------------------------------------

from __future__ import annotations
import sys
from pathlib import Path
import sqlite3
from datetime import datetime
import pandas as pd


# --- repo paths (relative) ---
REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR   = REPO_ROOT / "data" / "raw"
DB_PATH   = REPO_ROOT / "data" / "warehouse.db"
DDL_PATH  = REPO_ROOT / "sql" / "create_tables.sql"


def ensure_db_and_tables():
    """Create the SQLite DB + tables if missing (idempotent)."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn, open(DDL_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())


def read_daily_csv(for_date: str) -> pd.DataFrame:
    """Load data/raw/sessions_YYYY-MM-DD.csv as a DataFrame."""
    csv_path = RAW_DIR / f"sessions_{for_date}.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"missing file: {csv_path}")
    df = pd.read_csv(csv_path)

    # quick schema check (keep it simple)
    expected = ["player_id", "game_id", "session_start", "session_end"]
    if list(df.columns) != expected:
        raise ValueError(f"expected columns {expected}, got {list(df.columns)}")
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Compute session minutes; drop bad/null rows."""
    df = df.dropna(subset=["player_id", "session_start", "session_end"]).copy()
    df["session_start"] = pd.to_datetime(df["session_start"], errors="coerce")
    df["session_end"]   = pd.to_datetime(df["session_end"], errors="coerce")
    df = df.dropna(subset=["session_start", "session_end"])

    # minutes between start/end; clamp negatives to 0
    minutes = (df["session_end"] - df["session_start"]).dt.total_seconds() / 60.0
    df["session_minutes"] = minutes.clip(lower=0)
    return df


def aggregate(df: pd.DataFrame, for_date: str) -> pd.DataFrame:
    """Per-player totals for one day."""
    g = (
        df.groupby("player_id", as_index=False)
          .agg(total_sessions=("player_id", "count"),
               total_minutes =("session_minutes", "sum"))
    )
    g.insert(0, "dt", for_date)  # keep dt as simple string 'YYYY-MM-DD'
    return g[["dt", "player_id", "total_sessions", "total_minutes"]]


def load_fact(df_fact: pd.DataFrame, for_date: str):
    """
    Very simple load strategy:
    - delete existing rows for that dt
    - insert new aggregates
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM fact_player_sessions WHERE dt = ?", (for_date,))
        conn.commit()
        df_fact.to_sql("fact_player_sessions", conn, if_exists="append", index=False)


def main(for_date: str):
    # small guardrail: ensure format is YYYY-MM-DD
    try:
        datetime.strptime(for_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("for_date must be YYYY-MM-DD")

    ensure_db_and_tables()
    df_raw  = read_daily_csv(for_date)
    df_t    = transform(df_raw)
    df_fact = aggregate(df_t, for_date)
    load_fact(df_fact, for_date)
    print(f"loaded {len(df_fact)} fact rows for {for_date}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python src/etl.py YYYY-MM-DD")
        sys.exit(1)
    main(sys.argv[1])
