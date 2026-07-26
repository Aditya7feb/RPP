# Risk Analysis Examples

**File:** `skills/reporting/risk-analysis/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Risk Analysis Capability.

---

# Example 1 — Prioritize And Aggregate

## Request

```yaml
analyze:
  finding_refs:
    - finding-sqli-5001
    - finding-xss-5002
  risk_refs:
    - risk-sqli-3001
    - risk-xss-3002
  analysis:
    calculate_cvss: true
    normalize: true
    aggregate: true
    prioritize: true
    portfolio_metrics: true
  bounds:
    max_findings: 500
```

## Response

```yaml
analyze_result:
  analysis_ref: analysis-rp-9101
  derived_cvss:
    - finding: finding-sqli-5001
      cvss_vector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
      note: derived-for-presentation
  prioritized_findings:
    - finding-sqli-5001
    - finding-xss-5002
  aggregate_risk:
    critical: 1
    high: 1
  portfolio_metrics:
    mean_severity: high
  metrics_ref: metrics-rp-7101
```

The capability derives CVSS vectors and a prioritized, aggregated view for presentation. Canonical
Risk remains authoritative; derived values are marked as presentation figures.

---

# Example 2 — Derived Value Differs From Canonical

## Response

```yaml
analyze_result:
  analysis_ref: analysis-rp-9102
  derived_cvss:
    - finding: finding-idor-5010
      cvss_vector: "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N"
      note: differs-from-canonical-risk; canonical-authoritative
  metrics_ref: metrics-rp-7102
```

A calculated CVSS differs from the canonical Risk severity. The capability records the derived value
as presentation-only and defers to canonical Risk as authoritative.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
