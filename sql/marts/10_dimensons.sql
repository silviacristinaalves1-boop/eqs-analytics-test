--Dim_site
CREATE TABLE marts.dim_site (
    site_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    site_id INTEGER NOT NULL,
    site_name VARCHAR(255),
    country VARCHAR(10),
    region VARCHAR(50),
    business_unit VARCHAR(100),

    valid_from DATE NOT NULL,
    valid_to DATE NOT NULL,
    is_current BOOLEAN NOT NULL
);

--Dim metric
CREATE TABLE marts.dim_metric (
    metric_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    metric_code VARCHAR(50) NOT NULL,
    metric_name VARCHAR(255),
    category VARCHAR(100),
    canonical_uom VARCHAR(20),
    is_additive CHAR(1)
);

--Dim Date
CREATE TABLE marts.dim_date (
    date_key INTEGER PRIMARY KEY,
    month_start DATE NOT NULL,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    month_number INTEGER NOT NULL,
    month_name VARCHAR(20)
);

---Populate dimensions

---Dim msite
INSERT INTO marts.dim_site (
    site_id,
    site_name,
    country,
    region,
    business_unit,
    valid_from,
    valid_to,
    is_current
)
SELECT
    site_id,
    site_name,
    country,
    region,
    business_unit,
    DATE '1900-01-01',
    DATE '9999-12-31',
    TRUE
FROM staging.sites;

---Dim metric
INSERT INTO marts.dim_metric (
    metric_code,
    metric_name,
    category,
    canonical_uom,
    is_additive
)
SELECT
    metric_code,
    metric_name,
    category,
    canonical_uom,
    is_additive
FROM staging.metric_definitions;

--Dim Date
--Based on the months available in the readings table

INSERT INTO marts.dim_date (
    date_key,
    month_start,
    year,
    quarter,
    month_number,
    month_name
)
SELECT DISTINCT
    CAST(REPLACE(period, '-', '') || '01' AS INTEGER),
    TO_DATE(period || '-01', 'YYYY-MM-DD'),
    EXTRACT(YEAR FROM TO_DATE(period || '-01', 'YYYY-MM-DD')),
    EXTRACT(QUARTER FROM TO_DATE(period || '-01', 'YYYY-MM-DD')),
    EXTRACT(MONTH FROM TO_DATE(period || '-01', 'YYYY-MM-DD')),
    TO_CHAR(TO_DATE(period || '-01', 'YYYY-MM-DD'), 'Month')
FROM staging.readings;
