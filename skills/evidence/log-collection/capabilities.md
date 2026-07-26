# Log Collection Capabilities

**File:** `skills/evidence/log-collection/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Log Collection Capability. Each capability is
scope-confined, bounded, and produces no Findings or Risk.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| LC-1 | Source confinement | sources | Authorized sources |
| LC-2 | Log reading | sources, window | Read log events |
| LC-3 | Order preservation | log events | Ordered events |
| LC-4 | Redaction | log events | Redacted events |
| LC-5 | Artifact writing | events | Artifact |
| LC-6 | Evidence promotion | artifact | Evidence reference |
| LC-7 | Metrics emission | run | Metrics |

---

# LC-1 — Source Confinement

The capability SHALL confine collection to authorized sources within
[Scope](../../../schemas/scope.md).

---

# LC-2 — Log Reading

The capability SHALL read log events through the shared
[Logging](../../shared/logging/README.md) package, bounded by volume and window.

---

# LC-3 — Order Preservation

The capability SHALL preserve the ordering of collected log events.

---

# LC-4 — Redaction

The capability SHALL redact sensitive log content where configured before storage.

---

# LC-5 — Artifact Writing

The capability SHALL record collections as [Artifacts](../../../schemas/artifact.md) referencing
the [Log Event](../../../schemas/log-event.md) schema.

---

# LC-6 — Evidence Promotion

The capability SHALL invoke the shared [Evidence](../../shared/evidence/README.md) lifecycle to
promote collections into durable Evidence. The capability invokes promotion but does not own its
implementation.

---

# LC-7 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing collected log counts.

---

# Capability Boundaries

The capability SHALL NOT read or store logs directly, collect from unauthorized sources, interpret
content, own durable persistence, or produce Findings or Risk.

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface
operations in [interface.md](interface.md).
