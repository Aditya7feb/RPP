# HTTP Archive Execution

**File:** `skills/evidence/http-archive/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the HTTP Archive Capability.

---

# Execution Stages

```
Stage 1  Intake And Scope Validation
Stage 2  Policy Consultation
Stage 3  Transaction Collection
Stage 4  Redaction
Stage 5  Archive Writing And Evidence Promotion
Stage 6  Metrics Emission
```

---

# Stage 1 — Intake And Scope Validation

The capability SHALL validate that `target` is within [Scope](../../../schemas/scope.md).
Out-of-scope traffic SHALL be excluded before any request.

---

# Stage 2 — Policy Consultation

Before every request, the capability SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md). Only an `allow` decision permits the
request; `requires_approval` SHALL defer it; `deny` SHALL suppress it.

---

# Stage 3 — Transaction Collection

The capability SHALL collect HTTP transactions through the
[HTTP Client](../../shared/http-client/README.md) and, where configured, the
[Proxy](../../shared/proxy/README.md), honoring volume bounds.

---

# Stage 4 — Redaction

The capability SHALL redact credentials, tokens, and configured sensitive content.

---

# Stage 5 — Archive Writing And Evidence Promotion

The capability SHALL record transactions as [Artifacts](../../../schemas/artifact.md) of type
`http-archive` referencing the [HTTP Transaction](../../../schemas/http-transaction.md) schema, and
invoke the shared [Evidence](../../shared/evidence/README.md) lifecycle to promote the archive into
durable Evidence. Promotion is implemented by the shared Evidence infrastructure.

---

# Stage 6 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing archived transaction
counts.

---

# Determinism

Given identical captured transactions and redaction settings, the capability SHALL produce
equivalent archives.

---

# Idempotence

Archiving SHALL be non-destructive and SHALL NOT alter target state.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
