CREATE SCHEMA IF NOT EXISTS staging;

-- Sites
CREATE TABLE staging.sites (
    site_id INTEGER,
    site_name VARCHAR(255),
    country VARCHAR(10),
    region VARCHAR(50),
    business_unit VARCHAR(100)
);

-- Metric definitions
CREATE TABLE staging.metric_definitions (
    metric_code VARCHAR(50),
    metric_name VARCHAR(255),
    category VARCHAR(100),
    canonical_uom VARCHAR(20),
    is_additive CHAR(1)
);

-- UOM conversions
CREATE TABLE staging.uom_conversions (
    from_uom VARCHAR(20),
    to_uom VARCHAR(20),
    factor NUMERIC(18,6)
);

-- Readings
CREATE TABLE staging.readings (
    reading_id INTEGER,
    site_id INTEGER,
    period VARCHAR(7),
    metric_code VARCHAR(50),
    value NUMERIC(18,2),
    uom VARCHAR(20),
    period_type CHAR(1),
    source_system VARCHAR(50),
    submitted_at DATE
);

-- Incidents
CREATE TABLE staging.incidents (
    incident_id INTEGER,
    site_id INTEGER,
    incident_date DATE,
    incident_type VARCHAR(100),
    severity VARCHAR(20),
    is_recordable CHAR(1),
    lost_days INTEGER,
    reported_by VARCHAR(100)
);
