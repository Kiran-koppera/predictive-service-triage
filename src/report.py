"""Generate a stakeholder-facing markdown summary into reports/.

Evidence for the "summary reports" requirement in
docs/tesla_job_description.md.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"


def write_summary(model_report: str, n_incidents: int) -> Path:
      REPORTS_DIR.mkdir(parents=True, exist_ok=True)
      out_path = REPORTS_DIR / f"triage_summary_{date.today().isoformat()}.md"
      out_path.write_text(
          f"# Predictive Service Triage - Summary\n\n"
          f"Generated: {date.today().isoformat()}\n\n"
          f"Incidents scored: {n_incidents}\n\n"
          f"## Model performance\n\n```\n{model_report}\n```\n"
      )
      return out_path
  
