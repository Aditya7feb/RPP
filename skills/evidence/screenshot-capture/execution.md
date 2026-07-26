# Screenshot Capture Execution

**File:** `skills/evidence/screenshot-capture/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Screenshot Capture Capability.

---

# Execution Stages

```
Stage 1  Intake And Scope Validation
Stage 2  Policy Consultation
Stage 3  Page Rendering
Stage 4  Redaction
Stage 5  Artifact Emission And Evidence Promotion
Stage 6  Metrics Emission
```

---

# Stage 1 — Intake And Scope Validation

The capability SHALL validate that `target` is within [Scope](../../../schemas/scope.md).
Out-of-scope pages SHALL be rejected before any capture.

---

# Stage 2 — Policy Consultation

Before every capture, the capability SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md). Only an `allow` decision permits the
capture; `requires_approval` SHALL defer it; `deny` SHALL suppress it.

---

# Stage 3 — Page Rendering

The capability SHALL render the in-scope page through the
[Browser](../../shared/browser/README.md).

---

# Stage 4 — Redaction

The capability SHALL redact sensitive on-screen content where configured.

---

# Stage 5 — Artifact Emission And Evidence Promotion

The capability SHALL record the capture as an [Artifact](../../../schemas/artifact.md) of type
`screenshot` and invoke the shared [Evidence](../../shared/evidence/README.md) lifecycle to
promote it into durable Evidence. Promotion is implemented by the shared Evidence infrastructure.

---

# Stage 6 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing capture counts.

---

# Determinism

Given identical page state and options, the capability SHALL produce equivalent captures. Dynamic
page content SHALL be reflected faithfully.

---

# Idempotence

Capture SHALL be non-destructive and SHALL NOT alter target state.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
