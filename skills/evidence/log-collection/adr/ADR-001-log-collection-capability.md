# ADR-001 — Log Collection Capability

**File:** `skills/evidence/log-collection/adr/ADR-001-log-collection-capability.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

Assessments require durable log evidence — application, service, and infrastructure logs — with
preserved ordering. Log primitives are provided by the shared Logging package; collecting logs as
durable evidence is a distinct Evidence-tier collection capability that consumes those primitives
and must not own the durable evidence lifecycle.

---

# Decision

We SHALL provide a Log Collection Capability in the Evidence tier that reads log events through the
shared [Logging](../../../shared/logging/README.md) package; preserves ordering; records
collections as [Artifacts](../../../../schemas/artifact.md) referencing the
[Log Event](../../../../schemas/log-event.md) schema; invokes the shared
[Evidence](../../../shared/evidence/README.md) lifecycle to promote collections into durable
Evidence; and emits [Metrics](../../../../schemas/metrics.md). It produces no Findings or Risk and
does not own durable persistence, integrity, or retention.

---

# Consequences

## Positive

- Durable, ordered log evidence built on the shared Logging package.
- Bounded, redacted collection separated from interpretation and lifecycle.

## Negative

- Collection fidelity depends on the shared Logging package.

## Neutral

- Structured-field extraction is deferred to future extensions.

---

# Alternatives Considered

- Emitting or storing logs directly. Rejected because log primitives belong to the shared Logging
  package.
- Treating logs as generic artifacts in Artifact Collection. Rejected because logs have distinct
  ordering and windowing semantics and their own canonical schema.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [Logging](../../../shared/logging/README.md)
- [Evidence](../../../shared/evidence/README.md)
