# ADR-001 — Mutation Engine Capability

**File:** `skills/active-testing/mutation-engine/adr/ADR-001-mutation-engine-capability.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

Active testing requires transforming base inputs into bounded, reproducible sets of variants
for coverage. Embedding mutation logic in each consumer would duplicate strategies and lose
lineage and safety guarantees. Mutation is a reusable security capability, not a transport or
access client, so it belongs in the Active Testing tier.

---

# Decision

We SHALL provide a Mutation Engine Capability in the Active Testing tier that registers named
deterministic strategies; applies them to a base [Payload](../../../../schemas/payload.md)
within bounds; records lineage and preserves safety markers, including `requires_approval`
for destructive mutations; and emits derived Payloads and
[Metrics](../../../../schemas/metrics.md). It performs no target-facing action and produces no
Findings or Risk.

---

# Consequences

## Positive

- Reproducible, bounded variant generation with lineage and safety preserved.
- Reuse across active-testing and domain capabilities.

## Negative

- Requires strategy maintenance.

## Neutral

- Coverage-guided and grammar-aware mutation are deferred to future extensions.

---

# Alternatives Considered

- Per-consumer mutation logic. Rejected for duplication and inconsistent lineage.
- Placing mutation in shared infrastructure. Rejected because it is a reusable security
  capability, not a transport or access client, per the approved tier decision.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [Payload Schema](../../../../schemas/payload.md)
- [Metrics Schema](../../../../schemas/metrics.md)
