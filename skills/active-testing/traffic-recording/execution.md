# Traffic Recording Execution

**File:** `skills/active-testing/traffic-recording/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Traffic Recording Capability.

---

# Execution Stages

```
Stage 1  Intake And Scope Validation
Stage 2  Policy Consultation
Stage 3  Bounded Capture
Stage 4  Redaction
Stage 5  Artifact Writing And Metrics
```

---

# Stage 1 — Intake And Scope Validation

The capability SHALL validate that the selected exchanges are within
[Scope](../../../schemas/scope.md). Out-of-scope traffic SHALL be excluded.

---

# Stage 2 — Policy Consultation

The capability SHALL consult the [Policy Engine](../../shared/policy-engine/README.md) to
confirm recording authorization for the selected exchanges.

---

# Stage 3 — Bounded Capture

The capability SHALL capture exchanges through the [Proxy](../../shared/proxy/README.md),
honoring transaction and duration bounds.

---

# Stage 4 — Redaction

The capability SHALL redact credentials, tokens, and sensitive content before storage.

---

# Stage 5 — Artifact Writing And Metrics

The capability SHALL write [Artifacts](../../../schemas/artifact.md) with an integrity hash and
emit [Metrics](../../../schemas/metrics.md).

---

# Determinism

Given identical captured exchanges and redaction settings, the capability SHALL produce
equivalent artifacts.

---

# Idempotence

Recording SHALL NOT alter target state; it observes and stores exchanges.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
