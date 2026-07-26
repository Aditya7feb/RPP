# ADR-001 — Fuzzing Capability

**File:** `skills/active-testing/fuzzing/adr/ADR-001-fuzzing-capability.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

Web Security and API Security skills require bounded delivery of generated inputs to a target
and the resulting response corpora before they can interpret weaknesses. Delivering payloads
and recording responses is a reusable capability distinct from interpreting the results.
Fuzzing is a reusable security capability, not a transport or access client, so it belongs in
the Active Testing tier and drives the shared HTTP Client rather than issuing requests itself.

Because fuzzing is target-facing, every delivery must be gated by the Policy Engine, bounded in
volume and rate, non-destructive by default, and never a source of denial of service.

---

# Decision

We SHALL provide a Fuzzing Capability in the Active Testing tier that sources corpora from
[Payload Generation](../../payload-generation/README.md) and the
[Mutation Engine](../../mutation-engine/README.md); delivers them through the
[HTTP Client](../../../shared/http-client/README.md); gates every delivery through the
[Policy Engine](../../../shared/policy-engine/README.md), deferring payloads marked
`requires_approval`; and records responses as
[Observations](../../../../schemas/observation.md),
[Artifacts](../../../../schemas/artifact.md), and
[Metrics](../../../../schemas/metrics.md). It delivers non-destructively within bounds and
produces no Findings or Risk.

---

# Consequences

## Positive

- A governed, reusable delivery-and-recording capability for domain skills.
- Bounded, policy-gated, non-destructive delivery clearly separated from interpretation.

## Negative

- Coverage depends on corpus quality and delivery bounds.

## Neutral

- Coverage-guided and stateful sequence fuzzing are deferred to future extensions.

---

# Alternatives Considered

- Embedding delivery in each domain skill. Rejected for duplication and inconsistent gating.
- Placing fuzzing in shared infrastructure. Rejected because it is a reusable security
  capability, not a transport or access client, per the approved tier decision.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [Payload Generation](../../payload-generation/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
