# Reporting Capabilities

**File:** `skills/shared/reporting/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Reporting Shared Skill.
Capabilities describe *what* the shared skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[Reporting Interface](interface.md).

---

# Capability Model

```
Aggregation

Deduplication

Correlation

Ordering

Evidence Bundling

Composition

Rendering

Observability
```

---

# Aggregation Capabilities

## Finding Aggregation

The Reporting Shared Skill SHALL aggregate canonical
[Findings](../../../schemas/finding.md) across contributing skills.

---

## Provenance Preservation

The Reporting Shared Skill SHALL preserve each finding's provenance during
aggregation.

---

# Deduplication Capabilities

## Duplicate Detection

The Reporting Shared Skill SHALL detect findings describing the same issue at the
same location.

---

## Evidence Merging

The Reporting Shared Skill SHALL merge evidence references when deduplicating,
retaining the highest severity and confidence.

---

# Correlation Capabilities

## Finding Correlation

The Reporting Shared Skill SHALL group related findings into logical
correlations without altering their individual validity.

---

# Ordering Capabilities

## Severity Ordering

The Reporting Shared Skill SHALL order findings by severity and then by
confidence using declared scoring inputs.

---

# Evidence Bundling Capabilities

## Evidence Bundling

The Reporting Shared Skill SHALL bundle referenced
[Evidence](../../../schemas/evidence.md) through the
[Evidence](../evidence/README.md) shared package.

---

## Integrity Preservation

The Reporting Shared Skill SHALL preserve evidence integrity and redaction in
bundles.

---

# Composition Capabilities

## Canonical Report Composition

The Reporting Shared Skill SHALL compose a canonical
[Report](../../../schemas/report.md) independent of output format.

---

# Rendering Capabilities

## Multi-Format Rendering

The Reporting Shared Skill SHALL render the canonical report into structured and
document formats through adapters.

---

## Adapter Independence

The Reporting Shared Skill SHALL render without exposing renderer
implementations to consumers.

---

# Observability Capabilities

## Event Emission

The Reporting Shared Skill SHOULD publish lifecycle events to the Execution
State.

---

## Metrics

The Reporting Shared Skill SHOULD expose metrics including findings aggregated,
duplicates merged, correlations formed, and reports rendered.

---

# Capability Boundaries

The Reporting Shared Skill SHALL NOT

- Produce findings
- Reinterpret finding validity
- Invent risk scores
- Perform target-facing operations
- Expose redacted material in rendered output

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Finding Aggregation | Aggregation | SHALL |
| Provenance Preservation | Aggregation | SHALL |
| Duplicate Detection | Deduplication | SHALL |
| Evidence Merging | Deduplication | SHALL |
| Finding Correlation | Correlation | SHALL |
| Severity Ordering | Ordering | SHALL |
| Evidence Bundling | Evidence Bundling | SHALL |
| Integrity Preservation | Evidence Bundling | SHALL |
| Canonical Report Composition | Composition | SHALL |
| Multi-Format Rendering | Rendering | SHALL |
| Adapter Independence | Rendering | SHALL |
| Event Emission | Observability | SHOULD |
| Metrics | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Report Schema](../../../schemas/report.md)
