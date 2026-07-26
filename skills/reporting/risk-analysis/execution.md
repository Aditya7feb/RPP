# Risk Analysis Execution

**File:** `skills/reporting/risk-analysis/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Risk Analysis Capability.

---

# Execution Stages

```
Stage 1  Finding And Risk Loading
Stage 2  CVSS Calculation
Stage 3  Normalization And Aggregation
Stage 4  Prioritization
Stage 5  Portfolio Metrics
Stage 6  Analysis Writing And Metrics
```

---

# Stage 1 — Finding And Risk Loading

The capability SHALL load referenced [Findings](../../../schemas/finding.md) and
[Risk](../../../schemas/risk.md) by identifier, bounded by `max_findings`, without modifying them.

---

# Stage 2 — CVSS Calculation

The capability SHALL calculate CVSS vectors for presentation. Calculated vectors are derived and
SHALL NOT replace canonical Risk.

---

# Stage 3 — Normalization And Aggregation

The capability SHALL normalize scores across Findings and aggregate risk across scopes, presenting
results as derived values.

---

# Stage 4 — Prioritization

The capability SHALL prioritize Findings for presentation without altering canonical Risk.

---

# Stage 5 — Portfolio Metrics

The capability SHALL compute portfolio-level risk metrics for presentation.

---

# Stage 6 — Analysis Writing And Metrics

The capability SHALL produce analysis content for a [Report](../../../schemas/report.md) through the
shared [Reporting](../../shared/reporting/README.md) package and emit
[Metrics](../../../schemas/metrics.md). Derived values SHALL be distinguished from canonical Risk.

---

# Canonical Authority

Where a calculated value differs from canonical Risk, canonical Risk remains authoritative at every
stage. The capability SHALL NOT create, modify, or replace canonical Risk.

---

# Determinism

Given identical inputs and settings, the capability SHALL produce identical derived analysis.

---

# Idempotence

Analysis SHALL NOT modify the referenced Findings, Risk, or Evidence.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
