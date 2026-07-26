# Finding Mapping Execution

**File:** `skills/reporting/finding-mapping/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Finding Mapping Capability.

---

# Execution Stages

```
Stage 1  Finding Loading
Stage 2  OWASP Mapping
Stage 3  MITRE ATT&CK Mapping
Stage 4  Mapping Writing And Metrics
```

---

# Stage 1 — Finding Loading

The capability SHALL load referenced [Findings](../../../schemas/finding.md) by identifier, bounded
by `max_findings`, without modifying them.

---

# Stage 2 — OWASP Mapping

The capability SHALL map Findings to OWASP categories for presentation, referencing existing
classification such as CWE without altering it.

---

# Stage 3 — MITRE ATT&CK Mapping

The capability SHALL map Findings to MITRE ATT&CK techniques for presentation.

---

# Stage 4 — Mapping Writing And Metrics

The capability SHALL produce mapping content for a [Report](../../../schemas/report.md) through the
shared [Reporting](../../shared/reporting/README.md) package and emit
[Metrics](../../../schemas/metrics.md).

---

# Determinism

Given identical Findings and mapping references, the capability SHALL produce identical mappings.

---

# Idempotence

Mapping SHALL NOT modify the referenced Findings, Risk, or Evidence.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
