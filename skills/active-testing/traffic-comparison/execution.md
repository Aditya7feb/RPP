# Traffic Comparison Execution

**File:** `skills/active-testing/traffic-comparison/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Traffic Comparison Capability.

---

# Execution Stages

```
Stage 1  Load Recordings
Stage 2  Align Exchanges
Stage 3  Compute Differences
Stage 4  Apply Tolerance And Redaction
Stage 5  Emit Difference Artifact And Metrics
```

---

# Stage 1 — Load Recordings

The capability SHALL load the baseline and candidate recorded
[Artifacts](../../../schemas/artifact.md).

---

# Stage 2 — Align Exchanges

The capability SHALL align corresponding exchanges between the two recordings.

---

# Stage 3 — Compute Differences

The capability SHALL compute differences across the enabled dimensions, bounded by
`max_transactions`.

---

# Stage 4 — Apply Tolerance And Redaction

The capability SHALL apply tolerance settings to ignore expected variation and redact sensitive
content.

---

# Stage 5 — Emit Difference Artifact And Metrics

The capability SHALL emit a difference [Artifact](../../../schemas/artifact.md) of type
`traffic-diff` and [Metrics](../../../schemas/metrics.md). It SHALL NOT interpret differences or
emit Findings.

---

# Determinism

Given identical recordings, dimensions, tolerance, and bounds, the capability SHALL produce an
identical difference Artifact.

---

# Idempotence

Comparison SHALL contact no target and SHALL NOT alter the input recordings.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
