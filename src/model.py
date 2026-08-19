"""Train and evaluate a triage-priority classifier.

Evidence for "Predictive Triage & Machine Learning" in
docs/00_role_alignment.md.
"""
from __future__ import annotations

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

FEATURE_COLS = [
      "model_year",
      "odometer_km",
      "days_since_prev_event",
      "prior_incident_count",
]
LABEL_COL = "needs_priority_triage"


def train(df: pd.DataFrame) -> tuple[RandomForestClassifier, str]:
      df = df.dropna(subset=FEATURE_COLS + [LABEL_COL])
      X = df[FEATURE_COLS]
      y = df[LABEL_COL]
      X_train, X_test, y_train, y_test = train_test_split(
          X, y, test_size=0.2, random_state=42, stratify=y if y.nunique() > 1 else None
      )
      clf = RandomForestClassifier(n_estimators=200, random_state=42)
      clf.fit(X_train, y_train)
      report = classification_report(y_test, clf.predict(X_test))
      return clf, report
  
