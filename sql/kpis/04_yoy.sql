CREATE OR REPLACE VIEW marts.kpi_yoy AS
WITH emissions_group AS (
  SELECT
        period,
        'GROUP' AS grouping_level,
        'ALL' AS grouping_value,
        SUM(total_tco2e) AS total_tco2e
    FROM marts.kpi_emissions
    GROUP BY period
),
emissions_bu AS (
  SELECT
        period,
        'BUSINESS_UNIT' AS grouping_level,
        business_unit AS grouping_value,
        SUM(total_tco2e) AS total_tco2e
    FROM marts.kpi_emissions
    GROUP BY
        period,
        business_unit
),
base AS (
  SELECT * FROM emissions_group
  UNION ALL
  SELECT * FROM emissions_bu
),
yoy AS (
   SELECT
        period,
        grouping_level,
        grouping_value,
        total_tco2e,
        LAG(total_tco2e, 12) OVER (
            PARTITION BY grouping_level, grouping_value
            ORDER BY period
        ) AS total_tco2e_ly
    FROM base
)
SELECT
    period,
    grouping_level,
    grouping_value,
    total_tco2e,
    total_tco2e_ly,
    total_tco2e - total_tco2e_ly AS yoy_abs,
    (
        total_tco2e - total_tco2e_ly
    ) / NULLIF(total_tco2e_ly, 0) AS yoy_pct
  FROM yoy;
