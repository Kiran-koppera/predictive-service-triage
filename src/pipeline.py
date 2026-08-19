"""Orchestrates preprocessing -> features -> model -> report.

Run with: python -m src.pipeline
Requires a raw extract at data/raw/incident_triage_features.csv (see
sql/01_service_failure_queries.sql for the expected shape, or point this at
a real database export).
"""
from __future__ import annotations

from src import data_preprocessing, feature_engineering, model, report


def main() -> None:
      df = data_preprocessing.read_raw("incident_triage_features.csv")
      df = data_preprocessing.clean(df)
      df["event_ts"] = df["event_ts"].astype("datetime64[ns]")

    df = feature_engineering.add_recency_features(df)
    df = feature_engineering.add_severity_label(df)
    data_preprocessing.write_processed(df, "incident_triage_features.parquet")

    clf, model_report = model.train(df)
    print(model_report)

    out_path = report.write_summary(model_report, n_incidents=len(df))
    print(f"Wrote summary report to {out_path}")


if __name__ == "__main__":
      main()
  
