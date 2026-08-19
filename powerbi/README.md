Power BI Dashboard

This folder holds service_triage_dashboard.pbix (the BI evidence referenced in docs/00_role_alignment.md) plus the notes below documenting its data model. The .pbix itself is a binary file built in Power BI Desktop against the incident_triage_features view from sql/01_service_failure_queries.sql; it is added here once built locally, since it cannot be authored as plain text.

Data model

Tables imported from the incident_triage_features SQL view: fact_incidents (one row per telemetry-triggered incident: event, vehicle, ticket, warranty join), dim_vehicle (model, model year, region), and dim_date (standard date dimension for time-intelligence measures).

Key DAX measures

Incident Count = COUNTROWS(fact_incidents). Predicted High-Priority Rate = DIVIDE([High Priority Incidents], [Incident Count]). Avg Turnaround Days = AVERAGE(fact_incidents[turnaround_days]). Total Warranty Cost = SUM(fact_incidents[claim_amount]).

Dashboard pages

Overview: incident volume trend, predicted-severity mix, average turnaround by model and region. Root Cause: top symptom and event codes driving high-priority triage. Cost Impact: warranty cost by root cause and region.
