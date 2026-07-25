# Evidence Capabilities

**File:** `skills/shared/evidence/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Evidence Shared Skill.
Capabilities describe *what* the shared skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[Evidence Interface](interface.md).

---

# Capability Model

```
Composition

Artifact Storage

Integrity

Redaction

Scope And Retention

Referencing

Observability
```

---

# Composition Capabilities

## Evidence Composition

The Evidence Shared Skill SHALL compose canonical
[Evidence](../../../schemas/evidence.md) records from caller input.

---

## Deterministic Referencing

The Evidence Shared Skill SHALL issue stable, deterministic references for stored
evidence.

---

# Artifact Storage Capabilities

## Artifact Storage

The Evidence Shared Skill SHALL store large payloads as artifacts by reference.

---

## Reference Resolution

The Evidence Shared Skill SHALL resolve artifact references within the evidence
scope.

---

# Integrity Capabilities

## Integrity Sealing

The Evidence Shared Skill SHALL seal evidence with integrity metadata enabling
tamper detection.

---

## Immutability

The Evidence Shared Skill SHALL treat sealed evidence as immutable and SHALL
express corrections as new linked records.

---

# Redaction Capabilities

## Secret Redaction

The Evidence Shared Skill SHALL redact secret material before persistence.

---

## Redaction Recording

The Evidence Shared Skill SHALL record that redaction occurred and which fields
were affected.

---

# Scope And Retention Capabilities

## Scope Enforcement

The Evidence Shared Skill SHALL bound evidence visibility to its scope.

---

## Retention Enforcement

The Evidence Shared Skill SHALL dispose of expired evidence according to policy
while recording disposal.

---

# Referencing Capabilities

## Cross-Object Correlation

The Evidence Shared Skill SHALL enable correlation with
[Findings](../../../schemas/finding.md),
[Log Events](../../../schemas/log-event.md), and
[Reports](../../../schemas/report.md).

---

# Observability Capabilities

## Event Emission

The Evidence Shared Skill SHOULD publish lifecycle events to the Execution
State.

---

## Metrics

The Evidence Shared Skill SHOULD expose metrics including evidence captured,
artifacts stored, and evidence disposed.

---

# Capability Boundaries

The Evidence Shared Skill SHALL NOT

- Interpret evidence as a finding
- Decide risk
- Perform target-facing operations
- Persist secrets
- Mutate sealed evidence

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Evidence Composition | Composition | SHALL |
| Deterministic Referencing | Composition | SHALL |
| Artifact Storage | Artifact Storage | SHALL |
| Reference Resolution | Artifact Storage | SHALL |
| Integrity Sealing | Integrity | SHALL |
| Immutability | Integrity | SHALL |
| Secret Redaction | Redaction | SHALL |
| Redaction Recording | Redaction | SHALL |
| Scope Enforcement | Scope And Retention | SHALL |
| Retention Enforcement | Scope And Retention | SHALL |
| Cross-Object Correlation | Referencing | SHALL |
| Event Emission | Observability | SHOULD |
| Metrics | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Evidence Schema](../../../schemas/evidence.md)
