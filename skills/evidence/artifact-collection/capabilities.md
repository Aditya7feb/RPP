# Artifact Collection Capabilities

**File:** `skills/evidence/artifact-collection/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Artifact Collection Capability. Each capability is
scope-confined, bounded, and produces no Findings or Risk.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| AC-1 | Location confinement | sources | Authorized locations |
| AC-2 | Artifact reading | sources | Read artifacts |
| AC-3 | Type classification | artifacts | Typed artifacts |
| AC-4 | Redaction | artifacts | Redacted artifacts |
| AC-5 | Artifact writing | artifacts | Artifact |
| AC-6 | Evidence promotion | artifact | Evidence reference |
| AC-7 | Metrics emission | run | Metrics |

---

# AC-1 — Location Confinement

The capability SHALL confine collection to authorized locations within
[Scope](../../../schemas/scope.md).

---

# AC-2 — Artifact Reading

The capability SHALL read artifacts through the
[Filesystem Client](../../shared/filesystem-client/README.md), bounded by volume and size.

---

# AC-3 — Type Classification

The capability SHALL classify collected items as `file`, `certificate`, or other artifact types,
referencing the [Certificate](../../../schemas/certificate.md) and
[Certificate Chain](../../../schemas/certificate-chain.md) schemas for certificate artifacts.

---

# AC-4 — Redaction

The capability SHALL redact sensitive content where configured before storage.

---

# AC-5 — Artifact Writing

The capability SHALL record collected items as [Artifacts](../../../schemas/artifact.md).

---

# AC-6 — Evidence Promotion

The capability SHALL invoke the shared [Evidence](../../shared/evidence/README.md) lifecycle to
promote collected artifacts into durable Evidence. The capability invokes promotion but does not
own its implementation.

---

# AC-7 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing collected artifact
counts.

---

# Capability Boundaries

The capability SHALL NOT access the filesystem directly, collect from unauthorized locations,
interpret content, own durable persistence, or produce Findings or Risk.

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface
operations in [interface.md](interface.md).
