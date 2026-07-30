"""Data quality framework.

The runner and the report writer are provided. ONE example rule is implemented
so you can see the shape. The rest is yours.

Design intent: a data quality rule is *data*, not a branch in a function. A
sustainability controller who does not write Python should be able to read
RULES and understand what is being checked and what happens when it fails.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import duckdb
import pandas as pd

from .config import REPORTS_DIR

Severity = Literal["ERROR", "WARN", "INFO"]
Action = Literal["BLOCK", "QUARANTINE", "COERCE", "FLAG"]


@dataclass(frozen=True)
class Rule:
    rule_id: str
    rule_name: str
    severity: Severity
    action: Action
    # SQL returning ONE row: (rows_checked BIGINT, rows_failed BIGINT)
    check_sql: str
    # Optional SQL returning the offending rows, for the quarantine table.
    detail_sql: str | None = None


RULES: list[Rule] = [
    # ---------------------------------------------------------------- EXAMPLE
    Rule(
        rule_id="DQ001",
        rule_name="reading value is numeric",
        severity="ERROR",
        action="QUARANTINE",
        check_sql="""
            SELECT
                count(*)                                        AS rows_checked,
                count(*) FILTER (
                    WHERE try_cast(value AS DOUBLE) IS NULL
                )                                               AS rows_failed
            FROM raw.readings
        """,
        detail_sql="""
            SELECT reading_id, site_id, period, metric_code, value,
                   'value is not numeric' AS reason
            FROM raw.readings
            WHERE try_cast(value AS DOUBLE) IS NULL
        """,
    ),
    Rule(
    rule_id="DQ002",
    rule_name="site_id unique",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) - count(DISTINCT site_id) AS rows_failed
        FROM raw.sites
    """
    ),
    Rule(
    rule_id="DQ003",
    rule_name="country must be ISO-2 code",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) FILTER (
                WHERE length(country) <> 2
                   OR country <> upper(country)
            ) AS rows_failed
        FROM raw.sites
    """,
    detail_sql="""
        SELECT *,
               'invalid country code' AS reason
        FROM raw.sites
        WHERE length(country) <> 2
           OR country <> upper(country)
    """
),
 Rule(
    rule_id="DQ004",
    rule_name="valid_to after valid_from",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) FILTER (
                WHERE valid_to IS NOT NULL
                  AND valid_to < valid_from
            ) AS rows_failed
        FROM raw.sites
    """
) ,
Rule(
    rule_id="DQ005",
    rule_name="incident_id unique",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) - count(DISTINCT incident_id) AS rows_failed
        FROM raw.incidents
    """
),
 Rule(
    rule_id="DQ006",
    rule_name="site exists",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) FILTER (
                WHERE s.site_id IS NULL
            ) AS rows_failed
        FROM raw.incidents i
        LEFT JOIN raw.sites s
            ON i.site_id = s.site_id
    """
) ,
Rule(
    rule_id="DQ007",
    rule_name="lost days non negative",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) FILTER (
                WHERE lost_days < 0
            ) AS rows_failed
        FROM raw.incidents
    """
),
Rule(
    rule_id="DQ008",
    rule_name="incident date not in future",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) FILTER (
                WHERE incident_date > current_date
            ) AS rows_failed
        FROM raw.incidents
    """
),
Rule(
    rule_id="DQ009",
    rule_name="recordable flag valid",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) FILTER (
                WHERE is_recordable NOT IN ('Y','N')
            ) AS rows_failed
        FROM raw.incidents
    """
),
Rule(
    rule_id="DQ010",
    rule_name="metric code unique",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) - count(DISTINCT metric_code) AS rows_failed
        FROM raw.metrics
    """
),
Rule(
    rule_id="DQ011",
    rule_name="valid metric category",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) FILTER (
                WHERE category NOT IN (
                    'Emissions',
                    'Energy',
                    'Water',
                    'Waste',
                    'Safety'
                )
            ) AS rows_failed
        FROM raw.metrics
    """
),
 Rule(
    rule_id="DQ012",
    rule_name="uom not null",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) FILTER (
                WHERE canonical_uom IS NULL
                   OR trim(canonical_uom) = ''
            ) AS rows_failed
        FROM raw.metrics
    """
),
Rule(
    rule_id="DQ013",
    rule_name="uom conversion unique",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) - count(DISTINCT from_uom || '|' || to_uom) AS rows_failed
        FROM raw.uom_conversion
    """
),
Rule(
    rule_id="DQ014",
    rule_name="conversion factor positive",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) FILTER (
                WHERE factor <= 0
            ) AS rows_failed
        FROM raw.uom_conversion
    """
),
Rule(
    rule_id="DQ015",
    rule_name="uom not null",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) FILTER (
                WHERE from_uom IS NULL
                   OR to_uom IS NULL
            ) AS rows_failed
        FROM raw.uom_conversion
    """
),
Rule(
    rule_id="DQ016",
    rule_name="factor is numeric",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) FILTER (
                WHERE try_cast(factor AS DOUBLE) IS NULL
            ) AS rows_failed
        FROM raw.uom_conversion
    """
),
Rule(
    rule_id="DQ017",
    rule_name="reading id unique",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) - count(DISTINCT reading_id) AS rows_failed
        FROM raw.readings
    """
),
Rule(
    rule_id="DQ018",
    rule_name="metric exists",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) FILTER (
                WHERE m.metric_code IS NULL
            ) AS rows_failed
        FROM raw.readings r
        LEFT JOIN dim.metric m
            ON r.metric_code = m.metric_code
    """
),
Rule(
    rule_id="DQ019",
    rule_name="site exists",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) FILTER (
                WHERE s.site_id IS NULL
            ) AS rows_failed
        FROM raw.readings r
        LEFT JOIN dim.site s
            ON r.site_id = s.site_id
    """
),
Rule(
    rule_id="DQ020",
    rule_name="metric and uom consistent",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) FILTER (
                WHERE
                    (metric_code = 'ENERGY_CONS'  AND uom <> 'MWh')
                 OR (metric_code = 'WATER_WD'     AND uom <> 'm3')
                 OR (metric_code = 'HOURS_WORKED' AND uom <> 'hours')
                 OR (metric_code = 'SCOPE1_GHG'   AND uom <> 't')
                 OR (metric_code = 'SCOPE2_GHG'   AND uom <> 't')
                 OR (metric_code = 'WASTE_TOTAL'  AND uom <> 't')
            ) AS rows_failed
        FROM raw.readings
    """
),
 Rule(
    rule_id="DQ021",
    rule_name="valid source system",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) FILTER (
                WHERE source_system NOT IN (
                    'SAP_EHS',
                    'SITE_PORTAL',
                    'MANUAL_XLS'
                )
            ) AS rows_failed
        FROM raw.readings
    """
),
Rule(
    rule_id="DQ022",
    rule_name="period format yyyy-mm",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) FILTER (
                WHERE try_strptime(period, '%Y-%m') IS NULL
            ) AS rows_failed
        FROM raw.readings
    """
),
Rule(
    rule_id="DQ023",
    rule_name="one reading per site period metric",
    severity="ERROR",
    action="QUARANTINE",
    check_sql="""
        SELECT
            count(*) AS rows_checked,
            count(*) FILTER (
                WHERE cnt > 1
            ) AS rows_failed
        FROM (
            SELECT
                site_id,
                period,
                metric_code,
                count(*) AS cnt
            FROM raw.readings
            GROUP BY 1,2,3
        )
    """
)
    
    # ------------------------------------------------------------------ TODO
    # Add your rules below. Think about what would actually mislead the Group
    # Sustainability lead if it went unnoticed, and set severity accordingly.
    # Not every problem deserves to block the load - argue your choices in
    # DECISIONS.md.
]


def run_rules(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Execute every rule, persist offending rows, return the report frame."""
    results = []
    con.execute("DROP TABLE IF EXISTS staging.dq_quarantine")
    quarantine_created = False

    for rule in RULES:
        checked, failed = con.execute(rule.check_sql).fetchone()
        results.append(
            {
                "rule_id": rule.rule_id,
                "rule_name": rule.rule_name,
                "severity": rule.severity,
                "rows_checked": int(checked),
                "rows_failed": int(failed),
                "action_taken": rule.action if failed else "NONE",
            }
        )

        if rule.detail_sql and failed:
            payload = f"""
                SELECT '{rule.rule_id}' AS rule_id, *
                FROM ({rule.detail_sql})
            """
            if not quarantine_created:
                con.execute(
                    f"CREATE TABLE staging.dq_quarantine AS "
                    f"SELECT rule_id, reading_id, site_id, period, metric_code, "
                    f"CAST(value AS VARCHAR) AS value, reason FROM ({payload})"
                )
                quarantine_created = True
            else:
                con.execute(
                    f"INSERT INTO staging.dq_quarantine "
                    f"SELECT rule_id, reading_id, site_id, period, metric_code, "
                    f"CAST(value AS VARCHAR) AS value, reason FROM ({payload})"
                )

    return pd.DataFrame(
        results,
        columns=["rule_id", "rule_name", "severity",
                 "rows_checked", "rows_failed", "action_taken"],
    )


def write_dq_report(df: pd.DataFrame) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(REPORTS_DIR / "dq_report.csv", index=False)


def has_blocking_failures(df: pd.DataFrame) -> bool:
    """True if any rule with action BLOCK failed. Wire this in if you want the
    pipeline to refuse to publish - that is a judgement call, and we want to
    see which way you go and why."""
    return bool(((df["action_taken"] == "BLOCK") & (df["rows_failed"] > 0)).any())
