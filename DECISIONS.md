# Decisions & Reconciliation Note

## 1. What I would sign off on

| Figure | Confidence | Why |
|---------|---------|---------|
| Energy Consumption (ENERGY_CONS) | High | Values are numeric, mapped to a valid metric, and reported in the expected canonical unit (MWh). |
| Scope 1 GHG Emissions (SCOPE1_GHG) | High | Data passed critical validation checks, including metric validity, numeric values, and unit consistency. |
| Scope 2 GHG Emissions (SCOPE2_GHG) | High | Data met all critical quality requirements and is traceable to a valid reporting source. |
| Water Withdrawal (WATER_WD) | High | Values are reported in the canonical unit (m3) and passed all blocking quality checks. |
| Waste Generated (WASTE_TOTAL) | High | Data is complete and consistent with the metric definition and unit standards. |
| Hours Worked (HOURS_WORKED) | High | Values passed validation and are suitable for use in safety KPI calculations. |

## 2. Data quality decisions

Critical validation failures were classified as **ERROR / QUARANTINE** because they could materially affect reported KPI values or prevent reconciliation. Examples include:

- Non-numeric measurement values
- Missing or unknown site identifiers
- Missing or unknown metric codes
- Duplicate readings for the same site, period, and metric
- Invalid date ranges
- Incompatible units of measure

Records failing these checks are excluded from KPI calculations until corrected.

Non-critical issues were classified as **WARN / LOG** because they represent standardization or formatting problems that do not materially affect reported figures. Examples include:

- Country names not using ISO-2 codes (e.g. Germany instead of DE)
- Inconsistent capitalization (e.g. germany instead of DE)
- Minor master-data standardization issues

These records remain available for reporting but are logged for remediation.

## 3. Reconciliation conclusion

Based on the implemented validation framework, KPI values generated from records that passed all ERROR-level checks are suitable for management reporting and external audit review.

Remaining WARN-level issues relate primarily to reference-data standardization and do not materially impact KPI calculations. These items should be addressed as part of ongoing data-quality improvement activities.




