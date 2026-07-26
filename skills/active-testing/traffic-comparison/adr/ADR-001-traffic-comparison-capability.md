# ADR-001 — Traffic Comparison Capability

**File:** `skills/active-testing/traffic-comparison/adr/ADR-001-traffic-comparison-capability.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

Differential analysis of recorded traffic — comparing a baseline against a replayed or later
recording — is a common basis for domain skills to reason about behavioral change. Computing a
structured, redacted difference is a reusable capability distinct from recording, replaying, or
interpreting traffic. Traffic comparison is a reusable security capability, not a transport or
access client, so it belongs in the Active Testing tier. It contacts no target.

---

# Decision

We SHALL provide a Traffic Comparison Capability in the Active Testing tier that loads two
recorded [Artifacts](../../../../schemas/artifact.md); aligns corresponding exchanges; computes
status, header, timing, and body differences under tolerance settings; redacts sensitive
content; and emits a difference [Artifact](../../../../schemas/artifact.md) and
[Metrics](../../../../schemas/metrics.md). It contacts no target and produces no Findings or
Risk.

---

# Consequences

## Positive

- Deterministic, redacted, structured differences reusable by domain skills.
- Clear separation of difference computation from interpretation.

## Negative

- Comparison fidelity depends on recording alignability.

## Neutral

- Semantic body diffing and multi-way comparison are deferred to future extensions.

---

# Alternatives Considered

- Embedding comparison in each domain skill. Rejected for duplication.
- Placing traffic comparison in shared infrastructure. Rejected because it is a reusable security
  capability, not a transport or access client, per the approved tier decision.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [Traffic Recording](../../traffic-recording/README.md)
- [Artifact Schema](../../../../schemas/artifact.md)
