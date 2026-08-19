"""Feature engineering on top of the SQL incident_triage_features view.

Evidence for "Predictive Triage & Machine Learning" in
docs/00_role_alignment.md.
"""
from __future__ import annotations

import pandas as pd


def add_recency_features(df: pd.DataFrame) -> pd.DataFrame:
      """Add days-since-last-event and prior-incident-count per vehicle."""
      df = df.sort_values(["vehicle_id", "event_ts"]).copy()
      df["days_since_prev_event"] = (
          df.groupby("vehicle_id")["event_ts"].diff().dt.total_seconds() / 86400
      )
      df["prior_incident_count"] = df.groupby("vehicle_id").cumcount()
      return df


def add_severity_label(df: pd.DataFrame, high_cost_threshold: float = 1000.0) -> pd.DataFrame:
      """Derive a binary triage label: does this incident likely need
          high-priority routing (long turnaround or high warranty cost)?
              """
      df = df.copy()
      df["needs_priority_triage"] = (
          (df.get("turnaround_days", 0) > 3)
          | (df.get("claim_amount", 0).fillna(0) > high_cost_threshold)
      ).astype(int)
      return df
  
