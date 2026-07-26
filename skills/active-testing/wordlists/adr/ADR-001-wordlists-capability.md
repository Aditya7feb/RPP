# ADR-001 — Wordlists Capability

**File:** `skills/active-testing/wordlists/adr/ADR-001-wordlists-capability.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

Multiple capabilities and domain skills require curated candidate inputs — web paths,
parameter names, subdomains, and payload seeds. Without a governed source, each capability
would embed private copies, causing duplication, drift, and inconsistent provenance.

Wordlists are reusable data rather than transport or access clients, so they belong in the
Active Testing capability tier rather than in shared infrastructure. They perform no
target-facing action and produce no Findings.

---

# Decision

We SHALL provide a Wordlists Capability in the Active Testing tier that registers named,
versioned lists; supports selection, filtering, and bounded sampling; emits content as
[Artifacts](../../../../schemas/artifact.md) and candidate values as
[Payload](../../../../schemas/payload.md) seeds; and emits
[Metrics](../../../../schemas/metrics.md). It performs no target interaction and produces no
Findings or Risk.

---

# Consequences

## Positive

- A single governed, versioned source of candidate inputs.
- Deterministic, bounded selection with clear provenance.

## Negative

- Requires list registry maintenance.

## Neutral

- Weighted and context-ranked selection is deferred to future extensions.

---

# Alternatives Considered

- Embedding lists within each consuming capability. Rejected for duplication and drift.
- Placing wordlists in shared infrastructure. Rejected because they are reusable security
  capabilities, not transport or access clients, per the approved tier decision.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [Payload Schema](../../../../schemas/payload.md)
- [Artifact Schema](../../../../schemas/artifact.md)
