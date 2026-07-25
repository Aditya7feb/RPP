# Reporting Interface

**File:** `skills/shared/reporting/interface.md`

**Version:** 1.0.0

---

# Purpose

The Reporting Interface defines the canonical contract through which platform
components compose and render assessment reports.

The interface standardizes finding submission, composition options, evidence
bundling, and rendering while remaining independent of any renderer
implementation.

All consumers SHALL compose reports exclusively through this interface.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- Renderer Independent
- Versioned
- Observable
- Backward Compatible
- Deterministic

---

# Relationship

```
Master Agent

↓

Reporting Interface

↓

Reporting Shared Skill

↓

Format Adapters
```

The interface SHALL NOT expose or depend on renderer internals.

---

# Interface Overview

```
Metadata

↓

Finding Set

↓

Composition Options

↓

Render Request

↓

Execution Context

↓

Report Result

↓

Errors
```

---

# Metadata

Every invocation SHALL include

```yaml
request_id:

assessment_id:

timestamp:
```

Metadata enables tracing and auditing.

---

# Finding Set

Every invocation SHALL define

```yaml
findings:
```

`findings` SHALL be an array of references to canonical
[Findings](../../../schemas/finding.md), or the identifier of a finding
collection to aggregate.

Each finding SHALL retain its provenance.

---

# Composition Options

The caller MAY specify

```yaml
deduplicate:

correlate:

order_by:

include_evidence:
```

`deduplicate` and `correlate` SHALL gate deduplication and correlation.

`order_by` SHALL be one of `severity`, `confidence`, or `severity_then_confidence`.

`include_evidence` SHALL gate evidence bundling.

---

# Render Request

Every invocation SHALL define

```yaml
formats:
```

`formats` SHALL be an array of requested output formats, such as `json`,
`sarif`, `markdown`, or `pdf`.

An empty `formats` array SHALL produce only the canonical report model.

---

# Execution Context

The Reporting Shared Skill SHALL receive read-only context.

```yaml
execution_id:

parent_span:

variables:
```

The interface SHALL treat context as read-only.

---

# Report Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

report_ref:

rendered:

metrics:
```

`outcome` SHALL be one of

```
composed

partial

error
```

`report_ref` SHALL reference the canonical
[Report](../../../schemas/report.md).

`rendered` SHALL be an array of rendered output references keyed by format.

`partial` SHALL indicate the canonical report composed but one or more renders
failed.

---

# Evidence Bundling

When `include_evidence` is enabled, the interface SHALL bundle evidence through
the [Evidence](../evidence/README.md) shared package by reference.

Bundled evidence SHALL preserve integrity and redaction.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the Reporting error model](error-model.md).

A renderer failure SHALL NOT discard a successfully composed canonical report;
the result SHALL be `partial`.

---

# Determinism

Given identical findings, options, and evidence, the composed canonical report
SHALL be identical apart from timestamps and references.

---

# Compatibility

The interface SHALL remain stable across formats and renderers.

Consumers SHALL require no modification when renderers change.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL define

- Metadata
- Finding Set
- Render Request
- Execution Context
- Report Result

---

# Quality Requirements

The Reporting Interface SHALL

✓ Remain renderer independent

✓ Produce a canonical report model

✓ Preserve evidence integrity

✓ Support structured errors

✓ Preserve traceability

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Template descriptors
- Delta report requests
- Standards-enrichment directives

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Reporting Interface provides a stable, implementation-independent
contract through which all platform components compose and render traceable
reports across the Robust PenTest Platform.
