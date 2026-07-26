# Traffic Comparison Capabilities

**File:** `skills/active-testing/traffic-comparison/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Traffic Comparison Capability. Each capability
is deterministic, bounded, non-target-facing, and produces no Findings or Risk.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| TC-1 | Recording loading | baseline_ref, candidate_ref | Loaded recordings |
| TC-2 | Exchange alignment | recordings | Aligned pairs |
| TC-3 | Difference analysis | aligned pairs | Differences |
| TC-4 | Redaction | differences | Redacted differences |
| TC-5 | Artifact and metrics emission | run | Artifact, Metrics |

---

# TC-1 — Recording Loading

The capability SHALL load two recorded [Artifacts](../../../schemas/artifact.md).

---

# TC-2 — Exchange Alignment

The capability SHALL align corresponding exchanges between the baseline and candidate recordings.

---

# TC-3 — Difference Analysis

The capability SHALL compute status, header, timing, and body differences across the selected
dimensions, bounded by comparison scope.

---

# TC-4 — Redaction

The capability SHALL redact sensitive content in the difference output.

---

# TC-5 — Artifact And Metrics Emission

The capability SHALL emit a difference [Artifact](../../../schemas/artifact.md) of type
`traffic-diff` and [Metrics](../../../schemas/metrics.md) describing difference counts.

---

# Capability Boundaries

The capability SHALL NOT contact targets, record or replay traffic, interpret differences, or
produce Findings or Risk.

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface
operations in [interface.md](interface.md).
