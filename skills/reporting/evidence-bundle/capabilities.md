# Evidence Bundle Capabilities

**File:** `skills/reporting/evidence-bundle/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Evidence Bundle Capability. Each capability is
read-only over Evidence and produces no Findings or Risk.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| EB-1 | Evidence loading | evidence_refs | Loaded Evidence |
| EB-2 | Integrity verification | Evidence | Integrity status |
| EB-3 | Redaction | Evidence | Redacted evidence |
| EB-4 | Bundle assembly | Evidence | Bundle Artifact |
| EB-5 | Metrics emission | run | Metrics |

---

# EB-1 — Evidence Loading

The capability SHALL load referenced [Evidence](../../../schemas/evidence.md) by identifier without
modifying it.

---

# EB-2 — Integrity Verification

The capability SHALL verify evidence integrity references through the shared
[Evidence](../../shared/evidence/README.md) infrastructure.

---

# EB-3 — Redaction

The capability SHALL redact sensitive content where required for distribution.

---

# EB-4 — Bundle Assembly

The capability SHALL assemble the bundle through the shared
[Reporting](../../shared/reporting/README.md) package and record it as an
[Artifact](../../../schemas/artifact.md) of type `evidence-bundle`.

---

# EB-5 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing bundle contents.

---

# Capability Boundaries

The capability SHALL NOT create, modify, or replace Evidence, Findings, or Risk, capture evidence, or
own the durable evidence lifecycle.

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface operations
in [interface.md](interface.md).
