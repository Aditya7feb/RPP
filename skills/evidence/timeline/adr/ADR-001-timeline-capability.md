# ADR-001 — Timeline Capability

**File:** `skills/evidence/timeline/adr/ADR-001-timeline-capability.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

Assessments benefit from a chronological, causal view that correlates Observations and Evidence.
Producing this correlation is a distinct Evidence-tier capability. It is essential that the Timeline
remain **descriptive** — correlation only — and never perform interpretation, because vulnerability
inference, Finding classification, and Risk prioritization belong to Domain Security capabilities.

---

# Decision

We SHALL provide a Timeline Capability in the Evidence tier that loads referenced
[Observations](../../../../schemas/observation.md) and
[Evidence](../../../../schemas/evidence.md); orders them chronologically; correlates them and
maintains causal relationships; emits a timeline [Artifact](../../../../schemas/artifact.md) that
references canonical objects by ID; and MAY invoke the shared
[Evidence](../../../shared/evidence/README.md) lifecycle to promote the timeline. It emits
[Metrics](../../../../schemas/metrics.md).

The Timeline Capability SHALL NOT infer vulnerabilities, classify Findings, prioritize Risk, or
perform security analysis. It is descriptive, not analytical, and produces no Findings or Risk.

---

# Consequences

## Positive

- A chronological, causal correlation of evidence that domain skills can interpret.
- Strict descriptive boundary keeps interpretation with Domain Security capabilities.

## Negative

- Correlation fidelity depends on the completeness of referenced Observations and Evidence.

## Neutral

- Multi-assessment correlation and causal-graph export are deferred to future extensions.

---

# Alternatives Considered

- Allowing Timeline to infer or prioritize. Rejected because interpretation and prioritization
  belong to Domain Security capabilities; Timeline is descriptive only.
- Introducing a dedicated `timeline` schema. Rejected because a timeline is representable as an
  `artifact` of type `timeline` referencing Observation and Evidence IDs; no new schema is justified.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [Evidence](../../../shared/evidence/README.md)
- [Observation Schema](../../../../schemas/observation.md)
