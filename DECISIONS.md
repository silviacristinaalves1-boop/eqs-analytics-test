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

## 3. Data quality issues ranked by materiality

### High materiality
1. Missing or unknown site identifiers
   - Records cannot be assigned to a reporting entity.
   - Excluded from KPI calculations until corrected.

2. Duplicate measurements
   - Can overstate energy, emissions, water or waste figures.
   - Requires source-system reconciliation.

3. Invalid units of measure
   - Creates risk of incorrect aggregation and KPI distortion.

### Medium materiality
4. Invalid date ranges
   - Affects period allocation and comparability.

5. Missing metric codes
   - Prevents classification into reporting KPIs.

### Low materiality
6. Country code standardization issues
   - No direct impact on KPI values.
   - Impacts reporting consistency only.
  
## 4. Actions required from site controllers

- Submit records using approved metric codes only.
- Use canonical reporting units defined by Group Sustainability.
- Resolve duplicate submissions before reporting deadlines.
- Ensure site identifiers exist in the approved master-data list.
- Validate reporting periods before file submission.

## 5. What I would build next

- Automated data-quality scorecards by site.
- Trend and anomaly detection for KPI movements.
- Reconciliation dashboard showing rejected and corrected records.
- Data-quality KPIs for site-controller performance.

## Deliberately left out

- Predictive modelling.
- Non-material formatting corrections beyond logging.

## 4. Reconciliation conclusion

Based on the implemented validation framework, KPI values generated from records that passed all ERROR-level checks are suitable for management reporting and external audit review.

Remaining WARN-level issues relate primarily to reference-data standardization and do not materially impact KPI calculations. These items should be addressed as part of ongoing data-quality improvement activities.

## 5. Actions required from site controllers

- Submit records using approved metric codes only.
- Use canonical reporting units defined by Group Sustainability.
- Resolve duplicate submissions before reporting deadlines.
- Ensure site identifiers exist in the approved master-data list.
- Validate reporting periods before file submission.

## 6. What I would build next

- Automated data-quality scorecards by site.
- Reconciliation dashboard for rejected and corrected records.
- KPI trend and anomaly monitoring.

### Deliberately left out

- Predictive modelling.
- Machine-learning anomaly detection.
- Additional checks with limited impact on reported figures.

## 7. Site Dimension

Implemented as SCD Type 2.

Reason:
Sites may be acquired, divested, renamed, or reassigned over time. SCD Type 2 preserves the historical state of site attributes by creating a new version whenever a tracked attribute changes.

This approach ensures that historical sustainability metrics remain associated with the correct site context at the time of reporting, supporting accurate trend analysis, reconciliation, and auditability without modifying historical fact records.


