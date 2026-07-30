CREATE OR REPLACE VIEW marts.kpi_trir AS
WITH monthly_incidents AS (
    SELECT
        site_id,
        TO_CHAR(DATE_TRUNC('month', incident_date), 'YYYY-MM') AS period,
        COUNT(*) AS recordable_incidents
    FROM incidents
    WHERE is_recordable = 'Y'
    GROUP BY site_id,
             TO_CHAR(DATE_TRUNC('month', incident_date), 'YYYY-MM')
),
monthly_hours AS (
    SELECT
        site_id,
        period,
        value AS hours_worked
    FROM readings
    WHERE metric_code = 'HOURS_WORKED'
),
base AS (
    SELECT
        s.site_id,
        s.site_name,
        h.period,
        COALESCE(i.recordable_incidents, 0) AS recordable_incidents,
        h.hours_worked
    FROM monthly_hours h
    JOIN sites s
        ON h.site_id = s.site_id
    LEFT JOIN monthly_incidents i
        ON h.site_id = i.site_id
       AND h.period = i.period
),
rolling AS (
    SELECT
        period,
        site_id,
        site_name,
        SUM(recordable_incidents) OVER (
            PARTITION BY site_id
            ORDER BY period
            ROWS 11 PRECEDING
        ) AS recordable_incidents_r12,
        SUM(hours_worked) OVER (
            PARTITION BY site_id
            ORDER BY period
            ROWS 11 PRECEDING
        ) AS hours_worked_r12
    FROM base
  )
)
SELECT
    period,
    site_id,
    site_name,
    recordable_incidents_r12,
    hours_worked_r12,
    recordable_incidents_r12 * 200000.0
        / NULLIF(hours_worked_r12, 0) AS trir_r12,
    months_in_window = 12 AS has_full_window
FROM rolling;
