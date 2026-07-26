# ADR-001 — Replay Capability

**File:** `skills/active-testing/replay/adr/ADR-001-replay-capability.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

Reproducing target behavior from recorded traffic — for confirmation, differential analysis, or
regression — requires re-delivering exact exchanges. Reconstructing and re-delivering recorded
requests is a reusable capability distinct from recording or interpreting them. Replay is a
reusable security capability, not a transport or access client, so it belongs in the Active
Testing tier and drives the shared HTTP Client rather than issuing requests itself.

Because replay is target-facing, every delivery must be gated by the Policy Engine, bounded,
non-destructive by default, and never a source of denial of service.

---

# Decision

We SHALL provide a Replay Capability in the Active Testing tier that reconstructs requests from
[Traffic Recording](../../traffic-recording/README.md) artifacts; applies bounded,
safety-preserving adjustments; delivers through the
[HTTP Client](../../../shared/http-client/README.md); gates every delivery through the
[Policy Engine](../../../shared/policy-engine/README.md), deferring state-changing adjustments;
and records responses as [Observations](../../../../schemas/observation.md),
[Artifacts](../../../../schemas/artifact.md), and [Metrics](../../../../schemas/metrics.md). It
delivers non-destructively within bounds and produces no Findings or Risk.

---

# Consequences

## Positive

- Reproducible target behavior for confirmation and comparison.
- Bounded, policy-gated, non-destructive delivery separated from interpretation.

## Negative

- Faithful replay depends on recording completeness.

## Neutral

- Session-aware and timing-faithful replay are deferred to future extensions.

---

# Alternatives Considered

- Embedding replay in each domain skill. Rejected for duplication and inconsistent gating.
- Placing replay in shared infrastructure. Rejected because it is a reusable security capability,
  not a transport or access client, per the approved tier decision.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [Traffic Recording](../../traffic-recording/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
