# Replay Capabilities

**File:** `skills/active-testing/replay/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Replay Capability. Each capability is
scope-confined, policy-gated, bounded, and produces no Findings or Risk.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| RP-1 | Policy consultation | delivery | Decision |
| RP-2 | Recording sourcing | recording_ref | Reconstructed requests |
| RP-3 | Field adjustment | adjustments | Adjusted requests |
| RP-4 | Bounded delivery | target | Delivery interactions |
| RP-5 | Response recording | responses | Observations |
| RP-6 | Artifact and metrics emission | run | Artifacts, Metrics |

---

# RP-1 — Policy Consultation

The capability SHALL consult the [Policy Engine](../../shared/policy-engine/README.md) before
every delivery, deferring adjustments that could alter target state.

---

# RP-2 — Recording Sourcing

The capability SHALL reconstruct requests from
[Traffic Recording](../traffic-recording/README.md) artifacts.

---

# RP-3 — Field Adjustment

The capability SHALL apply bounded, safety-preserving field adjustments to reconstructed
requests.

---

# RP-4 — Bounded Delivery

The capability SHALL deliver reconstructed requests through the
[HTTP Client](../../shared/http-client/README.md), honoring volume and rate bounds and never
causing denial of service.

---

# RP-5 — Response Recording

The capability SHALL record replay responses as
[Observations](../../../schemas/observation.md).

---

# RP-6 — Artifact And Metrics Emission

The capability SHALL capture replay interactions as [Artifacts](../../../schemas/artifact.md)
and emit [Metrics](../../../schemas/metrics.md).

---

# Capability Boundaries

The capability SHALL NOT interpret responses, replay destructive exchanges without approval,
flood targets, or produce Findings or Risk.

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface
operations in [interface.md](interface.md).
