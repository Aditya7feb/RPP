# Screenshot Capture Capabilities

**File:** `skills/evidence/screenshot-capture/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Screenshot Capture Capability. Each capability is
scope-confined, policy-gated, bounded, and produces no Findings or Risk.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| SC-1 | Policy consultation | capture request | Decision |
| SC-2 | Page rendering | target | Rendered result |
| SC-3 | Redaction | rendered result | Redacted capture |
| SC-4 | Artifact emission | capture | Artifact |
| SC-5 | Evidence promotion | artifact | Evidence reference |
| SC-6 | Metrics emission | run | Metrics |

---

# SC-1 — Policy Consultation

The capability SHALL consult the [Policy Engine](../../shared/policy-engine/README.md) before every
capture.

---

# SC-2 — Page Rendering

The capability SHALL render in-scope pages through the [Browser](../../shared/browser/README.md).

---

# SC-3 — Redaction

The capability SHALL redact sensitive on-screen content where configured before storing a capture.

---

# SC-4 — Artifact Emission

The capability SHALL record captures as [Artifacts](../../../schemas/artifact.md) of type
`screenshot`.

---

# SC-5 — Evidence Promotion

The capability SHALL invoke the shared [Evidence](../../shared/evidence/README.md) lifecycle to
promote captures into durable Evidence. The capability invokes promotion but does not own its
implementation.

---

# SC-6 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing capture counts.

---

# Capability Boundaries

The capability SHALL NOT render pages directly, interpret content, own durable persistence, or
produce Findings or Risk.

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface
operations in [interface.md](interface.md).
