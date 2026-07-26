# ADR-001 — Traffic Recording Capability

**File:** `skills/active-testing/traffic-recording/adr/ADR-001-traffic-recording-capability.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

Replay, comparison, and several domain skills require exact captures of request and response
traffic. Capturing and storing traffic durably, with redaction and bounds, is a reusable
capability distinct from replaying or interpreting it. Traffic recording is a reusable security
capability, not a transport or access client, so it belongs in the Active Testing tier and taps
the shared Proxy rather than implementing its own capture path.

---

# Decision

We SHALL provide a Traffic Recording Capability in the Active Testing tier that captures
authorized, in-scope exchanges through the [Proxy](../../../shared/proxy/README.md); gates
recording through the [Policy Engine](../../../shared/policy-engine/README.md); redacts
sensitive content; writes durable [Artifacts](../../../../schemas/artifact.md) with integrity
hashes; and emits [Metrics](../../../../schemas/metrics.md). It records within bounds and
produces no Findings or Risk.

---

# Consequences

## Positive

- Exact, redacted, referenced captures reusable by replay, comparison, and domain skills.
- Bounded, policy-gated capture separated from interpretation.

## Negative

- Storage growth requires retention management.

## Neutral

- Field-level redaction policies are deferred to future extensions.

---

# Alternatives Considered

- Embedding capture in each consumer. Rejected for duplication and inconsistent redaction.
- Placing traffic recording in shared infrastructure. Rejected because it is a reusable security
  capability, not a transport or access client, per the approved tier decision.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [Proxy](../../../shared/proxy/README.md)
- [Artifact Schema](../../../../schemas/artifact.md)
