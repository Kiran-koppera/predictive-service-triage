"""Unit tests for the src/ pipeline transforms.

Evidence for "Reproducibility & MLOps Practices" in
docs/00_role_alignment.md.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.feature_engineering import add_severity_label, add_recency_features
from src.data_preprocessing import clean


def test_add_severity_label_flags_long_turnaround():
      df = pd.DataFrame({"turnaround_days": [1, 5], "claim_amount": [100, 200]})
      out = add_severity_label(df)
      assert out["needs_priority_triage"].tolist() == [0, 1]


def test_add_severity_label_flags_high_cost():
      df = pd.DataFrame({"turnaround_days": [1, 1], "claim_amount": [100, 5000]})
      out = add_severity_label(df)
      assert out["needs_priority_triage"].tolist() == [0, 1]


def test_add_recency_features_counts_prior_incidents():
      df = pd.DataFrame(
                {
                              "vehicle_id": ["A", "A", "B"],
                              "event_ts": pd.to_datetime(["2026-01-01", "2026-01-05", "2026-01-02"]),
                }
      )
      out = add_recency_features(df)
      counts = out.set_index(["vehicle_id", "event_ts"])["prior_incident_count"]
      assert counts.loc[("A", pd.Timestamp("2026-01-01"))] == 0
      assert counts.loc[("A", pd.Timestamp("2026-01-05"))] == 1


def test_clean_normalizes_column_names_and_drops_empty_rows():
      df = pd.DataFrame({" Vehicle ID ": ["V1", None], " Model ": ["S", None]})
      out = clean(df)
      assert list(out.columns) == ["vehicle id", "model"]
      assert len(out) == 1
  
