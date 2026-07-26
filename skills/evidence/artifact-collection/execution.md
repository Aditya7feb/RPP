# Artifact Collection Execution

**File:** `skills/evidence/artifact-collection/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Artifact Collection Capability.

---

# Execution Stages

```
Stage 1  Intake And Location Confinement
Stage 2  Bounded Artifact Reading
Stage 3  Type Classification
Stage 4  Redaction
Stage 5  Artifact Writing And Evidence Promotion
Stage 6  Metrics Emission
```

---

# Stage 1 — Intake And Location Confinement

The capability SHALL confine collection to authorized locations within
[Scope](../../../schemas/scope.md). Unauthorized locations SHALL be rejected before any read.

---

# Stage 2 — Bounded Artifact Reading

The capability SHALL read artifacts through the
[Filesystem Client](../../shared/filesystem-client/README.md), honoring artifact-count and size
bounds.

---

# Stage 3 — Type Classification

The capability SHALL classify collected items as `file`, `certificate`, or other types,
referencing the [Certificate](../../../schemas/certificate.md) and
[Certificate Chain](../../../schemas/certificate-chain.md) schemas for certificate artifacts.

---

# Stage 4 — Redaction

The capability SHALL redact sensitive content where configured.

---

# Stage 5 — Artifact Writing And Evidence Promotion

The capability SHALL record collected items as [Artifacts](../../../schemas/artifact.md) and invoke
the shared [Evidence](../../shared/evidence/README.md) lifecycle to promote them into durable
Evidence. Promotion is implemented by the shared Evidence infrastructure.

---

# Stage 6 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing collected artifact
counts.

---

# Determinism

Given identical sources, types, and bounds, the capability SHALL produce equivalent Artifacts.

---

# Idempotence

Collection SHALL NOT alter source content; it reads and records artifacts.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
