# Network Trace Execution

**File:** `skills/evidence/network-trace/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Network Trace Capability.

---

# Execution Stages

```
Stage 1  Intake And Scope Validation
Stage 2  Policy Consultation
Stage 3  Bounded Flow Capture
Stage 4  Redaction
Stage 5  Trace Writing And Evidence Promotion
Stage 6  Metrics Emission
```

---

# Stage 1 — Intake And Scope Validation

The capability SHALL validate that `target` is within [Scope](../../../schemas/scope.md).
Out-of-scope traffic SHALL be excluded before any capture.

---

# Stage 2 — Policy Consultation

Before every capture, the capability SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md). Only an `allow` decision permits the
capture; `requires_approval` SHALL defer it; `deny` SHALL suppress it.

---

# Stage 3 — Bounded Flow Capture

The capability SHALL capture packet and flow evidence through the
[TCP Client](../../shared/tcp-client/README.md) and
[UDP Client](../../shared/udp-client/README.md), honoring flow and duration bounds.

---

# Stage 4 — Redaction

The capability SHALL redact sensitive payload content where configured.

---

# Stage 5 — Trace Writing And Evidence Promotion

The capability SHALL record captures as [Artifacts](../../../schemas/artifact.md) of type
`network-trace` and invoke the shared [Evidence](../../shared/evidence/README.md) lifecycle to
promote them into durable Evidence. Promotion is implemented by the shared Evidence infrastructure.

---

# Stage 6 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing captured flow counts.

---

# Determinism

Given identical captured flows and redaction settings, the capability SHALL produce equivalent
traces. Live traffic variability SHALL be reflected faithfully.

---

# Idempotence

Capture SHALL be non-destructive and SHALL NOT alter target state.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
