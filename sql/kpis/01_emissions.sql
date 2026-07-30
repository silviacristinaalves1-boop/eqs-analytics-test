CREATE OR REPLACE VIEW marts.kpi_emissions AS
WITH emissions AS (
    SELECT
        period,
        site_id,
        SUM(CASE WHEN metric_code = 'SCOPE1_GHG'
                 THEN value END) AS scope1_tco2e,
        SUM(CASE WHEN metric_code = 'SCOPE2_GHG'
                 THEN value END) AS scope2_tco2e
    FROM readings
    WHERE metric_code IN ('SCOPE1_GHG','SCOPE2_GHG')
    GROUP BY period, site_id
)

SELECT
    e.period,
    s.site_id,
    s.site_name,
    s.business_unit,
    s.region,
    e.scope1_tco2e,
    e.scope2_tco2e,
    e.scope1_tco2e + e.scope2_tco2e AS total_tco2e
FROM emissions e
INNER JOIN sites s
    ON e.site_id = s.site_id;
