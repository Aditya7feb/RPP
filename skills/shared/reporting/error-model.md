# Reporting Error Model

**File:** `skills/shared/reporting/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the Reporting Shared Skill.

The error model classifies the failure conditions the shared skill MAY produce
and aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The Reporting Shared Skill SHALL

- Produce canonical, structured errors
- Preserve a successfully composed report even when rendering fails
- Never expose redacted material through errors or output
- Preserve traceability to evidence

---

# Error Categories

The Reporting Shared Skill maps its failures onto the canonical categories.

```
Configuration

Validation

Aggregation

Evidence

Composition

Rendering

Adapter

Internal
```

---

# Configuration Errors

Raised when configuration is invalid.

Conditions

- Invalid `order_by`
- Missing `tie_breaker`
- Redaction preservation disabled
- A renderer lacks a `format` or `kind`

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when a compose request is malformed.

Conditions

- No findings supplied
- A referenced finding does not conform to the
  [Finding schema](../../../schemas/finding.md)

Validation errors SHALL be non-retryable.

---

# Aggregation Errors

Raised when findings cannot be aggregated.

Conditions

- A finding reference cannot be resolved
- Conflicting provenance for the same finding identifier

Aggregation errors SHALL fail the request.

---

# Evidence Errors

Raised when referenced evidence cannot be bundled.

Conditions

- Evidence reference cannot be resolved
- Evidence fails integrity verification
- Evidence outside `bundle_scope`

Integrity failures SHALL prevent bundling the affected evidence and SHALL be
surfaced.

---

# Composition Errors

Raised when a canonical report cannot be composed.

Composition errors SHALL fail the request and SHALL NOT emit a partial canonical
report.

---

# Rendering Errors

Raised when a renderer fails.

Rendering errors SHALL NOT discard the canonical report. The outcome SHALL be
`partial`, and the failing format SHALL be reported.

Rendering errors MAY be retryable subject to configuration.

---

# Adapter Errors

Raised when an underlying renderer or store adapter fails unexpectedly.

Adapter errors SHALL be normalized so that consumers remain unaware of the
implementation.

---

# Internal Errors

Raised for unexpected conditions within the Reporting Shared Skill.

Internal errors SHALL be treated as non-retryable and SHOULD be reported for
diagnosis.

---

# Error Structure

Every error SHALL conform to the canonical error structure.

```yaml
category:

code:

message:

retryable:

format:

evidence_ref:
```

`category` SHALL be one of the canonical categories.

`retryable` SHALL indicate whether the operation MAY be attempted again.

Errors SHALL NOT contain secret or redacted material.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| invalid_order | Configuration | No |
| redaction_disabled | Configuration | No |
| no_findings | Validation | No |
| malformed_finding | Validation | No |
| finding_unresolved | Aggregation | No |
| evidence_unresolved | Evidence | Policy dependent |
| evidence_tampered | Evidence | No |
| composition_failed | Composition | No |
| render_failed | Rendering | Policy dependent (partial) |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# Partial Composition Principle

A rendering failure SHALL NOT invalidate a successfully composed canonical
report.

The Reporting Shared Skill SHALL return the canonical report with a `partial`
outcome and identify the formats that failed so they MAY be retried.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [Report Schema](../../../schemas/report.md)
- [Finding Schema](../../../schemas/finding.md)
