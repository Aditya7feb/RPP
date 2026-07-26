# Risk Analysis Capabilities

**File:** `skills/reporting/risk-analysis/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Risk Analysis Capability. Each capability is
read-only over Findings and canonical Risk and never creates, modifies, or replaces canonical Risk.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| RA-1 | Finding and Risk loading | finding_refs, risk_refs | Loaded inputs |
| RA-2 | CVSS calculation | Findings | Derived CVSS vectors |
| RA-3 | Score normalization | Risk | Normalized scores |
| RA-4 | Risk aggregation | Risk | Aggregate views |
| RA-5 | Prioritization | Findings, Risk | Prioritized order |
| RA-6 | Portfolio metrics | Findings, Risk | Portfolio metrics |
| RA-7 | Analysis writing and metrics | run | Report content, Metrics |

---

# RA-1 — Finding And Risk Loading

The capability SHALL load referenced [Findings](../../../schemas/finding.md) and
[Risk](../../../schemas/risk.md) by identifier without modifying them.

---

# RA-2 — CVSS Calculation

The capability SHALL calculate CVSS vectors for presentation. Calculated vectors are derived figures
and SHALL NOT replace canonical Risk.

---

# RA-3 — Score Normalization

The capability SHALL normalize scores across Findings for comparison, presenting them as derived
values.

---

# RA-4 — Risk Aggregation

The capability SHALL aggregate risk across Findings and scopes for presentation.

---

# RA-5 — Prioritization

The capability SHALL prioritize Findings for presentation without altering canonical Risk.

---

# RA-6 — Portfolio Metrics

The capability SHALL compute portfolio-level risk metrics for presentation.

---

# RA-7 — Analysis Writing And Metrics

The capability SHALL produce analysis content for a [Report](../../../schemas/report.md) through the
shared [Reporting](../../shared/reporting/README.md) package and emit
[Metrics](../../../schemas/metrics.md).

---

# Capability Boundaries

The capability SHALL NOT create, modify, or replace canonical [Risk](../../../schemas/risk.md),
modify Findings or Evidence, produce Findings, or present derived values as canonical Risk. Where a
derived value differs from canonical Risk, canonical Risk remains authoritative.

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface operations
in [interface.md](interface.md).
