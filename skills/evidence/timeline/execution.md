# Timeline Execution

**File:** `skills/evidence/timeline/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Timeline Capability.

---

# Execution Stages

```
Stage 1  Reference Loading
Stage 2  Chronological Ordering
Stage 3  Correlation
Stage 4  Causal Linking
Stage 5  Timeline Writing And Evidence Promotion
Stage 6  Metrics Emission
```

---

# Stage 1 — Reference Loading

The capability SHALL load referenced [Observations](../../../schemas/observation.md) and
[Evidence](../../../schemas/evidence.md) by ID, bounded by `max_items`.

---

# Stage 2 — Chronological Ordering

The capability SHALL order the referenced items chronologically, preserving chronology.

---

# Stage 3 — Correlation

The capability SHALL correlate items relating to the same events or entities. Correlation is
descriptive and SHALL NOT interpret security meaning.

---

# Stage 4 — Causal Linking

The capability SHALL maintain causal relationships between correlated items where configured.

---

# Stage 5 — Timeline Writing And Evidence Promotion

The capability SHALL emit a timeline [Artifact](../../../schemas/artifact.md) of type `timeline`
referencing canonical objects by ID, and MAY invoke the shared
[Evidence](../../shared/evidence/README.md) lifecycle to promote it into durable Evidence. Promotion
is implemented by the shared Evidence infrastructure.

---

# Stage 6 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing correlation counts.

---

# Determinism

Given identical references and correlation settings, the capability SHALL produce an identical
timeline.

---

# Idempotence

Correlation SHALL NOT alter the referenced Observations or Evidence.

---

# Analytical Boundary

The capability SHALL NOT infer vulnerabilities, classify Findings, prioritize Risk, or perform
security analysis at any stage. Timeline is descriptive correlation only.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
