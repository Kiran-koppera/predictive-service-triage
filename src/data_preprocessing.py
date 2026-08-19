"""Load and clean raw extracts into data/processed/.

Evidence for "Data Pipelines & Workflow Automation" in
docs/00_role_alignment.md. Swap read_raw()'s source with a real
telemetry / service-ticket / warranty extract (or a DB connection defined
in config/) once data is available.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"


def read_raw(filename: str) -> pd.DataFrame:
      """Read a raw CSV extract from data/raw/."""
      path = RAW_DIR / filename
      if not path.exists():
                raise FileNotFoundError(
                              f"Expected raw file at {path}. Add a real or sample extract "
                              "before running the pipeline."
                )
            return pd.read_csv(path)


def clean(df: pd.DataFrame) -> pd.DataFrame:
      """Basic cleaning: drop empty rows, normalize column names."""
    df = df.dropna(how="all").copy()
    df.columns = [c.strip().lower() for c in df.columns]
    return df


def write_processed(df: pd.DataFrame, filename: str) -> Path:
      PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROCESSED_DIR / filename
    df.to_parquet(out_path, index=False)
    return out_path
