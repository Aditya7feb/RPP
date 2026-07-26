# ADR-001 — Payload Generation Capability

**File:** `skills/active-testing/payload-generation/adr/ADR-001-payload-generation-capability.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

Active testing and several domain skills require concrete, governed test inputs composed from
templates, wordlist seeds, and mutation variants. Constructing payloads ad hoc in each
consumer causes duplication, inconsistent encoding and safety marking, and lost lineage.
Payload generation is a reusable security capability, not a transport or access client, so it
belongs in the Active Testing tier.

---

# Decision

We SHALL provide a Payload Generation Capability in the Active Testing tier that composes
[Payloads](../../../../schemas/payload.md) from templates, [Wordlists](../../wordlists/README.md)
seeds, and [Mutation Engine](../../mutation-engine/README.md) variants; applies encoding and
non-destructive safety marking; references markers and out-of-band values rather than inlining
them; and emits Payloads and [Metrics](../../../../schemas/metrics.md). It performs no
target-facing action and produces no Findings or Risk.

---

# Consequences

## Positive

- Governed, reproducible, lineage-preserving payloads with consistent safety marking.
- Reuse across active-testing and domain capabilities.

## Negative

- Requires template registry maintenance.

## Neutral

- Grammar-driven and coverage-guided generation are deferred to future extensions.

---

# Alternatives Considered

- Per-consumer payload construction. Rejected for duplication and inconsistent safety.
- Placing payload generation in shared infrastructure. Rejected because it is a reusable
  security capability, not a transport or access client, per the approved tier decision.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [Wordlists](../../wordlists/README.md)
- [Mutation Engine](../../mutation-engine/README.md)
