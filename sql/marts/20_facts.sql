--fact_eqs_monthly
CREATE TABLE marts.fact_eqs_monthly (
    site_key INTEGER NOT NULL,
    date_key INTEGER NOT NULL,
    metric_key INTEGER NOT NULL,
    metric_value NUMERIC(18,6) NOT NULL,
    PRIMARY KEY (
        site_key,
        date_key,
        metric_key
    ),
  FOREIGN KEY (site_key)
        REFERENCES marts.dim_site(site_key),
  FOREIGN KEY (date_key)
        REFERENCES marts.dim_date(date_key),
  FOREIGN KEY (metric_key)
        REFERENCES marts.dim_metric(metric_key)
);

---populate the fact table
INSERT INTO marts.fact_eqs_monthly (
    site_key,
    date_key,
    metric_key,
    metric_value
)
SELECT
    ds.site_key,
    dd.date_key,
    dm.metric_key,
    r.value
FROM staging.readings r
INNER JOIN marts.dim_site s
    ON r.site_id = s.site_id
   AND ds.is_current = TRUE
INNER JOIN marts.dim_metric m
    ON r.metric_code = m.metric_code
INNER JOIN marts.dim_date dt
    ON dt.month_start =
       TO_DATE(r.period || '-01', 'YYYY-MM-DD');


--fact_incident
CREATE TABLE marts.fact_incident (
    incident_id INTEGER PRIMARY KEY,
    site_key INTEGER NOT NULL,
    date_key INTEGER NOT NULL,
    incident_count INTEGER NOT NULL,
    lost_days INTEGER NOT NULL,
    incident_type VARCHAR(100),
    severity VARCHAR(20),
    is_recordable CHAR(1),
    reported_by VARCHAR(100);
    FOREIGN KEY (site_key)
        REFERENCES marts.dim_site(site_key),
    FOREIGN KEY (date_key)
        REFERENCES marts.dim_date(date_key)
);

---populate the fact table
INSERT INTO marts.fact_incident (
    incident_id,
    site_key,
    date_key,
    incident_count,
    lost_days,
    incident_type 
    severity 
    is_recordable 
)
SELECT
    i.incident_id,
    ds.site_key,
    dd.date_key,
    1,
    i.lost_days,
    i.incident_type,    
    i.severity,
    i.is_recordable,
    i.reported_by
FROM staging.incidents i
JOIN marts.dim_site s
    ON i.site_id = s.site_id
   AND ds.is_current = TRUE
JOIN marts.dim_date dt
    ON dt.month_start =
       DATE_TRUNC('month', i.incident_date);
