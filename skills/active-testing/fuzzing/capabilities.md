# Fuzzing Capabilities

**File:** `skills/active-testing/fuzzing/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Fuzzing Capability. Each capability is
scope-confined, policy-gated, bounded, and produces no Findings or Risk.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| FZ-1 | Policy consultation | delivery | Decision |
| FZ-2 | Corpus sourcing | corpus_ref | Payload sequence |
| FZ-3 | Bounded delivery | surface | Delivery interactions |
| FZ-4 | Response recording | responses | Observations |
| FZ-5 | Artifact emission | interactions | Artifacts |
| FZ-6 | Metrics emission | run | Metrics |

---

# FZ-1 — Policy Consultation

The capability SHALL consult the [Policy Engine](../../shared/policy-engine/README.md) before
every delivery, deferring any payload marked `requires_approval`.

---

# FZ-2 — Corpus Sourcing

The capability SHALL source a corpus through
[Payload Generation](../payload-generation/README.md) and the
[Mutation Engine](../mutation-engine/README.md).

---

# FZ-3 — Bounded Delivery

The capability SHALL deliver payloads across the target surface through the
[HTTP Client](../../shared/http-client/README.md), honoring request and rate bounds and never
causing denial of service.

---

# FZ-4 — Response Recording

The capability SHALL record responses and behavioral signals as
[Observations](../../../schemas/observation.md).

---

# FZ-5 — Artifact Emission

The capability SHALL capture request and response interactions as
[Artifacts](../../../schemas/artifact.md).

---

# FZ-6 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing delivery counts,
timing, and coverage.

---

# Capability Boundaries

The capability SHALL NOT interpret responses as vulnerabilities, deliver destructive payloads
without approval, flood targets, or produce Findings or Risk.

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface
operations in [interface.md](interface.md).
