# Report Generation Execution

**File:** `skills/reporting/report-generation/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Report Generation Capability.

---

# Execution Stages

```
Stage 1  Input Loading
Stage 2  Composition (Executive Or Technical)
Stage 3  Serialization
Stage 4  Report Writing And Metrics
```

---

# Stage 1 — Input Loading

The capability SHALL load referenced [Findings](../../../schemas/finding.md),
[Risk](../../../schemas/risk.md), [Evidence](../../../schemas/evidence.md), and correlation,
analysis, and mapping content by identifier without modifying them.

---

# Stage 2 — Composition (Executive Or Technical)

The capability SHALL compose the report for the requested audience. Derived risk figures SHALL be
distinguished from canonical Risk.

---

# Stage 3 — Serialization

The capability SHALL serialize the [Report](../../../schemas/report.md) to the requested formats
through the shared [Reporting](../../shared/reporting/README.md) package. Formats are serializations,
not capabilities.

---

# Stage 4 — Report Writing And Metrics

The capability SHALL produce a [Report](../../../schemas/report.md) referencing canonical objects by
identifier and emit [Metrics](../../../schemas/metrics.md).

---

# Determinism

Given identical inputs, template, and formats, the capability SHALL produce an identical Report and
serializations.

---

# Idempotence

Generation SHALL NOT modify the referenced Findings, Risk, or Evidence.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
