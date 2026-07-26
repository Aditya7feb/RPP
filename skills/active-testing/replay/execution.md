# Replay Execution

**File:** `skills/active-testing/replay/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Replay Capability.

---

# Execution Stages

```
Stage 1  Intake And Scope Validation
Stage 2  Recording Reconstruction
Stage 3  Field Adjustment
Stage 4  Policy Consultation (per delivery)
Stage 5  Bounded Delivery
Stage 6  Emit Observations, Artifacts, And Metrics
```

---

# Stage 1 — Intake And Scope Validation

The capability SHALL validate that `target` is within [Scope](../../../schemas/scope.md).
Out-of-scope targets SHALL be rejected before any delivery.

---

# Stage 2 — Recording Reconstruction

The capability SHALL reconstruct requests from the referenced
[Traffic Recording](../traffic-recording/README.md) artifact.

---

# Stage 3 — Field Adjustment

The capability SHALL apply bounded, safety-preserving adjustments. Adjustments that could alter
target state SHALL be marked to require approval.

---

# Stage 4 — Policy Consultation (per delivery)

Before every delivery, the capability SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md). Only an `allow` decision permits
delivery; `requires_approval` SHALL defer it; `deny` SHALL suppress it.

---

# Stage 5 — Bounded Delivery

The capability SHALL deliver reconstructed requests through the
[HTTP Client](../../shared/http-client/README.md), honoring volume and rate bounds and never
causing denial of service.

---

# Stage 6 — Emit Observations, Artifacts, And Metrics

The capability SHALL record responses as [Observations](../../../schemas/observation.md), capture
interactions as [Artifacts](../../../schemas/artifact.md), and emit
[Metrics](../../../schemas/metrics.md). It SHALL NOT interpret responses or emit Findings.

---

# Determinism

Given identical recording, adjustments, bounds, and target behavior, the capability SHALL produce
identical Observations.

---

# Idempotence

Replay SHALL be non-destructive by default and SHALL NOT alter target state beyond bounded,
approved interactions.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
