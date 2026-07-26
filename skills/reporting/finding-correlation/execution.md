# Finding Correlation Execution

**File:** `skills/reporting/finding-correlation/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Finding Correlation Capability.

---

# Execution Stages

```
Stage 1  Finding Loading
Stage 2  Deduplication
Stage 3  Relation
Stage 4  Attack-Chain Construction
Stage 5  Correlation Writing And Metrics
```

---

# Stage 1 — Finding Loading

The capability SHALL load referenced [Findings](../../../schemas/finding.md) by identifier, bounded
by `max_findings`, without modifying them.

---

# Stage 2 — Deduplication

The capability SHALL group Findings describing the same underlying issue, referencing them by
identifier.

---

# Stage 3 — Relation

The capability SHALL relate Findings sharing a target, root cause, or attack path.

---

# Stage 4 — Attack-Chain Construction

The capability SHALL construct attack chains from related Findings, preserving ordering.

---

# Stage 5 — Correlation Writing And Metrics

The capability SHALL produce correlation content for a [Report](../../../schemas/report.md) through
the shared [Reporting](../../shared/reporting/README.md) package and emit
[Metrics](../../../schemas/metrics.md).

---

# Determinism

Given identical Findings and settings, the capability SHALL produce identical correlation content.

---

# Idempotence

Correlation SHALL NOT modify the referenced Findings, Risk, or Evidence.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
