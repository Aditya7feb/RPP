# Evidence Bundle Execution

**File:** `skills/reporting/evidence-bundle/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Evidence Bundle Capability.

---

# Execution Stages

```
Stage 1  Evidence Loading
Stage 2  Integrity Verification
Stage 3  Redaction
Stage 4  Bundle Assembly
Stage 5  Bundle Writing And Metrics
```

---

# Stage 1 — Evidence Loading

The capability SHALL load referenced [Evidence](../../../schemas/evidence.md) by identifier, bounded
by `max_evidence`, without modifying it.

---

# Stage 2 — Integrity Verification

The capability SHALL verify evidence integrity references through the shared
[Evidence](../../shared/evidence/README.md) infrastructure.

---

# Stage 3 — Redaction

The capability SHALL redact sensitive content where required for distribution.

---

# Stage 4 — Bundle Assembly

The capability SHALL assemble the bundle through the shared
[Reporting](../../shared/reporting/README.md) package, referencing Evidence by identifier.

---

# Stage 5 — Bundle Writing And Metrics

The capability SHALL record the bundle as an [Artifact](../../../schemas/artifact.md) of type
`evidence-bundle` and emit [Metrics](../../../schemas/metrics.md).

---

# Determinism

Given identical Evidence references and settings, the capability SHALL produce an equivalent bundle.

---

# Idempotence

Bundling SHALL NOT modify the referenced Evidence, Findings, or Risk.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
