# ADR-001 — Parameter Mining Capability

**File:** `skills/active-testing/parameter-mining/adr/ADR-001-parameter-mining-capability.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

Web Security and API Security skills require the set of request parameters a target accepts
before they can evaluate weaknesses. Discovering that parameter surface through bounded,
non-destructive probing is a reusable capability distinct from interpreting the parameters.
Parameter mining is a reusable security capability, not a transport or access client, so it
belongs in the Active Testing tier and drives the shared HTTP Client rather than issuing
requests itself.

---

# Decision

We SHALL provide a Parameter Mining Capability in the Active Testing tier that draws candidates
from [Wordlists](../../wordlists/README.md); probes query, body, header, and cookie locations
through the [HTTP Client](../../../shared/http-client/README.md); gates every request through
the [Policy Engine](../../../shared/policy-engine/README.md); and reports accepted, reflected,
or behavior-changing parameters as [Observations](../../../../schemas/observation.md),
[Artifacts](../../../../schemas/artifact.md), and [Metrics](../../../../schemas/metrics.md). It
performs non-destructive, bounded probing and produces no Findings or Risk.

---

# Consequences

## Positive

- A governed, reusable parameter-discovery surface for domain skills and Fuzzing.
- Bounded, policy-gated, non-destructive probing with clear separation from interpretation.

## Negative

- Discovery breadth depends on candidate quality and request bounds.

## Neutral

- Behavior-differential tuning is deferred to future extensions.

---

# Alternatives Considered

- Embedding parameter discovery in each domain skill. Rejected for duplication and inconsistent
  gating.
- Placing parameter mining in shared infrastructure. Rejected because it is a reusable security
  capability, not a transport or access client, per the approved tier decision.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
