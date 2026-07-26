# ADR-001 — Network Trace Capability

**File:** `skills/evidence/network-trace/adr/ADR-001-network-trace-capability.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

Assessments require transport-level network evidence — packet and flow captures — that is distinct
from application-layer HTTP evidence. Capturing network traffic is a separate collection capability
operating at a lower layer than HTTP Archive, and it must not own the durable evidence lifecycle.

---

# Decision

We SHALL provide a Network Trace Capability in the Evidence tier that captures packet and flow
evidence through the shared [TCP Client](../../../shared/tcp-client/README.md) and
[UDP Client](../../../shared/udp-client/README.md); gates every capture through the
[Policy Engine](../../../shared/policy-engine/README.md); records captures as
[Artifacts](../../../../schemas/artifact.md) of type `network-trace`; invokes the shared
[Evidence](../../../shared/evidence/README.md) lifecycle to promote traces into durable Evidence;
and emits [Metrics](../../../../schemas/metrics.md). It produces no Findings or Risk and does not
own durable persistence, integrity, or retention.

---

# Consequences

## Positive

- Transport-level evidence distinct from HTTP evidence, with durability via the shared lifecycle.
- Bounded, policy-gated, redacted capture separated from interpretation.

## Negative

- Capture fidelity depends on the shared transport clients.

## Neutral

- Encrypted-flow metadata capture is deferred to future extensions.

---

# Alternatives Considered

- Folding network traces into HTTP Archive. Rejected because they operate at different layers.
- Opening transport connections directly. Rejected because transport belongs to the shared TCP and
  UDP clients.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [TCP Client](../../../shared/tcp-client/README.md)
- [Evidence](../../../shared/evidence/README.md)
