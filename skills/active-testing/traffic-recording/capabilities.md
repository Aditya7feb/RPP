# Traffic Recording Capabilities

**File:** `skills/active-testing/traffic-recording/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Traffic Recording Capability. Each capability
is scope-confined, policy-gated, bounded, and produces no Findings or Risk.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| TR-1 | Policy consultation | scope_selector | Decision |
| TR-2 | Traffic capture | scope_selector | Captured exchanges |
| TR-3 | Redaction | exchanges | Redacted content |
| TR-4 | Artifact writing | exchanges | Artifacts |
| TR-5 | Metrics emission | run | Metrics |

---

# TR-1 — Policy Consultation

The capability SHALL consult the [Policy Engine](../../shared/policy-engine/README.md) to
confirm recording is authorized for the selected in-scope exchanges.

---

# TR-2 — Traffic Capture

The capability SHALL capture request and response exchanges through the
[Proxy](../../shared/proxy/README.md), bounded by volume and duration.

---

# TR-3 — Redaction

The capability SHALL redact sensitive content before storage.

---

# TR-4 — Artifact Writing

The capability SHALL write captured traffic as [Artifacts](../../../schemas/artifact.md) of
type `traffic-recording`.

---

# TR-5 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing captured counts and
duration.

---

# Capability Boundaries

The capability SHALL NOT generate, deliver, or replay traffic, interpret it, or produce
Findings or Risk.

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface
operations in [interface.md](interface.md).
