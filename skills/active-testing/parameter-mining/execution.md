# Parameter Mining Execution

**File:** `skills/active-testing/parameter-mining/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Parameter Mining Capability.

---

# Execution Stages

```
Stage 1  Intake And Scope Validation
Stage 2  Policy Consultation
Stage 3  Candidate Sourcing
Stage 4  Bounded Probing
Stage 5  Acceptance Detection
Stage 6  Emit Observations, Artifacts, And Metrics
```

---

# Stage 1 — Intake And Scope Validation

The capability SHALL validate that `target` is within [Scope](../../../schemas/scope.md).
Out-of-scope targets SHALL be rejected before any request.

---

# Stage 2 — Policy Consultation

Before every request, the capability SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md). Only an `allow` decision permits the
request; `requires_approval` SHALL defer it; `deny` SHALL suppress it.

---

# Stage 3 — Candidate Sourcing

The capability SHALL draw bounded candidate parameter names from
[Wordlists](../wordlists/README.md).

---

# Stage 4 — Bounded Probing

The capability SHALL issue non-destructive probes across the enabled locations through the
[HTTP Client](../../shared/http-client/README.md), honoring request bounds and rate ceilings.

---

# Stage 5 — Acceptance Detection

The capability SHALL detect accepted, reflected, or behavior-changing parameters and record
them as [Observations](../../../schemas/observation.md).

---

# Stage 6 — Emit Observations, Artifacts, And Metrics

The capability SHALL emit [Observations](../../../schemas/observation.md),
[Artifacts](../../../schemas/artifact.md), and [Metrics](../../../schemas/metrics.md). It SHALL
NOT interpret parameters or emit Findings.

---

# Determinism

Given identical target behavior, candidate set, and bounds, the capability SHALL produce
identical Observations.

---

# Idempotence

Probing SHALL be non-destructive and SHALL NOT alter target state.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
