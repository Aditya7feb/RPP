# Network Trace Capabilities

**File:** `skills/evidence/network-trace/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Network Trace Capability. Each capability is
scope-confined, policy-gated, bounded, and produces no Findings or Risk.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| NT-1 | Policy consultation | capture request | Decision |
| NT-2 | Flow capture | selection | Captured flows |
| NT-3 | Redaction | flows | Redacted flows |
| NT-4 | Trace writing | flows | Artifact |
| NT-5 | Evidence promotion | artifact | Evidence reference |
| NT-6 | Metrics emission | run | Metrics |

---

# NT-1 — Policy Consultation

The capability SHALL consult the [Policy Engine](../../shared/policy-engine/README.md) before every
capture.

---

# NT-2 — Flow Capture

The capability SHALL capture packet and flow evidence through the
[TCP Client](../../shared/tcp-client/README.md) and
[UDP Client](../../shared/udp-client/README.md), bounded by volume and duration.

---

# NT-3 — Redaction

The capability SHALL redact sensitive payload content where configured before storage.

---

# NT-4 — Trace Writing

The capability SHALL record captures as [Artifacts](../../../schemas/artifact.md) of type
`network-trace`.

---

# NT-5 — Evidence Promotion

The capability SHALL invoke the shared [Evidence](../../shared/evidence/README.md) lifecycle to
promote traces into durable Evidence. The capability invokes promotion but does not own its
implementation.

---

# NT-6 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing captured flow counts.

---

# Capability Boundaries

The capability SHALL NOT open transport connections directly, interpret traffic, own durable
persistence, or produce Findings or Risk.

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface
operations in [interface.md](interface.md).
