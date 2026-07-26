# Log Collection Execution

**File:** `skills/evidence/log-collection/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Log Collection Capability.

---

# Execution Stages

```
Stage 1  Intake And Source Confinement
Stage 2  Bounded Log Reading
Stage 3  Order Preservation
Stage 4  Redaction
Stage 5  Artifact Writing And Evidence Promotion
Stage 6  Metrics Emission
```

---

# Stage 1 — Intake And Source Confinement

The capability SHALL confine collection to authorized sources within
[Scope](../../../schemas/scope.md). Unauthorized sources SHALL be rejected before any read.

---

# Stage 2 — Bounded Log Reading

The capability SHALL read log events through the shared
[Logging](../../shared/logging/README.md) package, honoring event-count and window bounds.

---

# Stage 3 — Order Preservation

The capability SHALL preserve the ordering of collected log events.

---

# Stage 4 — Redaction

The capability SHALL redact sensitive log content where configured.

---

# Stage 5 — Artifact Writing And Evidence Promotion

The capability SHALL record collections as [Artifacts](../../../schemas/artifact.md) referencing
the [Log Event](../../../schemas/log-event.md) schema and invoke the shared
[Evidence](../../shared/evidence/README.md) lifecycle to promote them into durable Evidence.
Promotion is implemented by the shared Evidence infrastructure.

---

# Stage 6 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing collected log counts.

---

# Determinism

Given identical sources, window, and bounds, the capability SHALL produce equivalent, ordered
collections.

---

# Idempotence

Collection SHALL NOT alter source logs; it reads and records log events.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
