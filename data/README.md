Data

raw/ holds untouched source extracts (telemetry, service tickets, warranty claims). processed/ holds cleaned, model-ready tables written by src/data_preprocessing.py. Both are gitignored: nothing under data/ is committed except this file and the .gitkeep placeholders, since real vehicle and customer data should never live in source control. See sql/01_service_failure_queries.sql for the schema these files are expected to match, and docs/LOG.md for where to source or simulate a sample dataset.
