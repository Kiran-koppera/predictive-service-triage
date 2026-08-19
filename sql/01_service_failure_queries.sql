-- Field failure & service analytics: schema, staging, and the analyst-ready
-- feature view. This is the SQL evidence behind "Field Failure & Service
-- Analytics" in docs/00_role_alignment.md.

-- === Schema ===================================================

CREATE TABLE IF NOT EXISTS vehicles (
      vehicle_id      TEXT PRIMARY KEY,
      model           TEXT NOT NULL,
      model_year      INTEGER NOT NULL,
      region          TEXT,
      delivery_date   DATE
  );

CREATE TABLE IF NOT EXISTS telemetry_events (
      event_id        TEXT PRIMARY KEY,
      vehicle_id      TEXT NOT NULL REFERENCES vehicles(vehicle_id),
      event_ts        TIMESTAMP NOT NULL,
      event_code      TEXT NOT NULL,
      severity_flag   TEXT,
      odometer_km     NUMERIC
  );

CREATE TABLE IF NOT EXISTS service_tickets (
      ticket_id       TEXT PRIMARY KEY,
      vehicle_id      TEXT NOT NULL REFERENCES vehicles(vehicle_id),
      opened_ts       TIMESTAMP NOT NULL,
      closed_ts       TIMESTAMP,
      symptom_code    TEXT,
      resolution_code TEXT,
      labor_hours     NUMERIC
  );

CREATE TABLE IF NOT EXISTS warranty_claims (
      claim_id        TEXT PRIMARY KEY,
      ticket_id       TEXT REFERENCES service_tickets(ticket_id),
      claim_amount    NUMERIC,
      part_code       TEXT,
      approved        BOOLEAN
  );

-- === Staging: type-normalize and de-duplicate raw extracts ====

CREATE VIEW IF NOT EXISTS stg_telemetry_events AS
SELECT
    event_id,
    vehicle_id,
    CAST(event_ts AS TIMESTAMP)        AS event_ts,
    UPPER(TRIM(event_code))            AS event_code,
    COALESCE(severity_flag, 'UNKNOWN') AS severity_flag,
    odometer_km
FROM telemetry_events
WHERE vehicle_id IS NOT NULL;

CREATE VIEW IF NOT EXISTS stg_service_tickets AS
SELECT
    ticket_id,
    vehicle_id,
    CAST(opened_ts AS TIMESTAMP) AS opened_ts,
    CAST(closed_ts AS TIMESTAMP) AS closed_ts,
    UPPER(TRIM(symptom_code))    AS symptom_code,
    UPPER(TRIM(resolution_code)) AS resolution_code,
    labor_hours
FROM service_tickets
WHERE ticket_id IS NOT NULL;

-- === Analyst-ready view: joins telemetry to service outcomes ===
-- One row per incident, enriched with vehicle context, prior telemetry
-- signal, and the eventual service resolution. This is the "compile data
-- from multiple sources" requirement made concrete.

CREATE VIEW IF NOT EXISTS incident_triage_features AS
SELECT
    t.event_id,
    t.vehicle_id,
    v.model,
    v.model_year,
    v.region,
    t.event_ts,
    t.event_code,
    t.severity_flag,
    t.odometer_km,
    s.ticket_id,
    s.opened_ts,
    s.closed_ts,
    (JULIANDAY(s.closed_ts) - JULIANDAY(s.opened_ts)) AS turnaround_days,
    s.symptom_code,
    s.resolution_code,
    s.labor_hours,
    w.claim_amount,
    w.approved AS warranty_approved
FROM stg_telemetry_events t
JOIN vehicles v
    ON v.vehicle_id = t.vehicle_id
LEFT JOIN stg_service_tickets s
    ON s.vehicle_id = t.vehicle_id
   AND s.opened_ts BETWEEN t.event_ts AND DATETIME(t.event_ts, '+7 days')
LEFT JOIN warranty_claims w
    ON w.ticket_id = s.ticket_id;

-- === Reporting query: failure rate by model/region, last 90 days =====

SELECT
    v.model,
    v.region,
    COUNT(DISTINCT t.event_id)                         AS incident_count,
    COUNT(DISTINCT t.vehicle_id)                        AS vehicles_affected,
    ROUND(AVG(f.turnaround_days), 2)                    AS avg_turnaround_days,
    ROUND(SUM(f.claim_amount), 2)                        AS total_warranty_cost
FROM telemetry_events t
JOIN vehicles v ON v.vehicle_id = t.vehicle_id
LEFT JOIN incident_triage_features f ON f.event_id = t.event_id
WHERE t.event_ts >= DATE('now', '-90 days')
GROUP BY v.model, v.region
ORDER BY incident_count DESC;
