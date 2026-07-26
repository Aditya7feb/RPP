# Timeline Capabilities

**File:** `skills/evidence/timeline/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Timeline Capability. Each capability is
descriptive, correlation-only, and produces no Findings or Risk.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| TL-1 | Reference loading | observation_refs, evidence_refs | Loaded references |
| TL-2 | Chronological ordering | references | Ordered sequence |
| TL-3 | Correlation | references | Correlated items |
| TL-4 | Causal linking | references | Causal relationships |
| TL-5 | Timeline writing | correlation | Artifact |
| TL-6 | Metrics emission | run | Metrics |

---

# TL-1 — Reference Loading

The capability SHALL load referenced [Observations](../../../schemas/observation.md) and
[Evidence](../../../schemas/evidence.md) by ID.

---

# TL-2 — Chronological Ordering

The capability SHALL order referenced items chronologically, preserving chronology.

---

# TL-3 — Correlation

The capability SHALL correlate Observations and Evidence that relate to the same events or
entities.

---

# TL-4 — Causal Linking

The capability SHALL maintain causal relationships between correlated items where configured.

---

# TL-5 — Timeline Writing

The capability SHALL emit a timeline [Artifact](../../../schemas/artifact.md) of type `timeline`
that references canonical objects by ID and does not duplicate their content.

---

# TL-6 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing correlation counts.

---

# Capability Boundaries

The capability SHALL NOT infer vulnerabilities, classify Findings, prioritize Risk, perform
security analysis, interpret meaning, or produce Findings or Risk. Timeline is descriptive
correlation only.

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface
operations in [interface.md](interface.md).
