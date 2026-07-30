CREATE OR REPLACE VIEW marts.kpi_energy_intensity AS
WITH energy AS (
    SELECT
        period,
        site_id,
        value AS energy_mwh
    FROM readings
    WHERE metric_code = 'ENERGY_CONS'
),
hours AS (
    SELECT
        period,
        site_id,
        value AS hours_worked
    FROM readings
    WHERE metric_code = 'HOURS_WORKED'
)

SELECT
    e.period,
    s.site_id,
    s.site_name,
    e.energy_mwh,
    h.hours_worked,
    CASE
        WHEN h.hours_worked IS NULL THEN NULL
        WHEN h.hours_worked = 0 THEN NULL
        ELSE (e.energy_mwh * 1000.0) / h.hours_worked
    END AS mwh_per_1000_hours,
    FALSE AS is_estimated
FROM energy e
LEFT JOIN hours h
    ON e.site_id = h.site_id
   AND e.period = h.period
INNER JOIN sites s
    ON e.site_id = s.site_id;
