# src/query_results.py
# ------------------------------------------------------------
# Simple script to query and display ETL results
# from the fact_player_sessions table in SQLite.
#
# Usage:
#   python src/query_results.py
# ------------------------------------------------------------

import sqlite3
import pandas as pd
from pathlib import Path

# locate your warehouse db relative to repo root
REPO_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = REPO_ROOT / "data" / "warehouse.db"

def show_results():
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}. Run the ETL first!")
        return

    conn = sqlite3.connect(DB_PATH)
    try:
        query = "SELECT * FROM fact_player_sessions ORDER BY dt, player_id;"
        df = pd.read_sql(query, conn)
        if df.empty:
            print("fact_player_sessions is empty.")
        else:
            print(df)
    finally:
        conn.close()

if __name__ == "__main__":
    show_results()
