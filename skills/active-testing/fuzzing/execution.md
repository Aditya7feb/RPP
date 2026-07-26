# Fuzzing Execution

**File:** `skills/active-testing/fuzzing/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Fuzzing Capability.

---

# Execution Stages

```
Stage 1  Intake And Scope Validation
Stage 2  Corpus Resolution
Stage 3  Policy Consultation (per delivery)
Stage 4  Bounded Delivery
Stage 5  Response Recording
Stage 6  Emit Observations, Artifacts, And Metrics
```

---

# Stage 1 — Intake And Scope Validation

The capability SHALL validate that `target` is within [Scope](../../../schemas/scope.md).
Out-of-scope targets SHALL be rejected before any delivery.

---

# Stage 2 — Corpus Resolution

The capability SHALL resolve `corpus_ref` from
[Payload Generation](../payload-generation/README.md) and the
[Mutation Engine](../mutation-engine/README.md).

---

# Stage 3 — Policy Consultation (per delivery)

Before every delivery, the capability SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md). Only an `allow` decision permits
delivery; `requires_approval`, including for payloads marked `requires_approval`, SHALL defer
it; `deny` SHALL suppress it.

---

# Stage 4 — Bounded Delivery

The capability SHALL deliver payloads through the
[HTTP Client](../../shared/http-client/README.md), honoring request, rate, and duration bounds
and never causing denial of service.

---

# Stage 5 — Response Recording

The capability SHALL record responses and behavioral signals as
[Observations](../../../schemas/observation.md).

---

# Stage 6 — Emit Observations, Artifacts, And Metrics

The capability SHALL emit [Observations](../../../schemas/observation.md),
[Artifacts](../../../schemas/artifact.md), and [Metrics](../../../schemas/metrics.md). It SHALL
NOT interpret responses or emit Findings.

---

# Determinism

Given identical corpus, bounds, and target behavior, the capability SHALL produce identical
Observations. Non-deterministic target behavior SHALL be reflected faithfully in artifacts.

---

# Idempotence

Delivery SHALL be non-destructive by default and SHALL NOT alter target state beyond bounded,
approved interactions.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
