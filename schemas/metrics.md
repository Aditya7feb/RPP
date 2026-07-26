# Metrics Schema

**File:** `schemas/metrics.md`

**Version:** 1.0.0

---

# Purpose

The Metrics Schema defines the canonical, implementation-independent representation of
quantitative measurements produced during an assessment within the Robust PenTest Platform
(RPP).

Metrics record counts, timings, rates, and coverage produced by a capability's execution,
such as the number of payloads delivered, request throughput, or parameter-coverage ratios.
Metrics quantify execution; they do not interpret it.

A Metrics object represents measurement data only. It SHALL NOT contain security
interpretation, findings, risk, or secrets.

---

# Design Principles

A Metrics object SHALL be

- Quantitative and objective
- Traceable to its producing capability
- Unit-explicit
- Immutable once recorded
- Auditable
- Implementation independent

---

# Identity

Every Metrics object SHALL contain

```yaml
metrics_id:

assessment_id:

task_id:

schema_version:
```

`metrics_id` SHALL be unique within an assessment. `assessment_id` SHALL reference the
owning [assessment](assessment.md). `task_id` SHALL reference the producing
[task](task.md). `schema_version` SHALL be `1.0.0`.

---

# Scope

Every Metrics object SHALL contain

```yaml
scope:
  capability:
  window:
```

`capability` SHALL name the capability that produced the measurements. `window` SHALL
describe the measurement window, such as a start and end time or an execution identifier.

---

# Measurements

Every Metrics object SHALL contain

```yaml
measurements:
```

`measurements` SHALL be a namespaced list where each entry contains

```yaml
name:
value:
unit:
```

`name` SHALL identify the measurement, such as `payloads.delivered` or
`requests.per_second`. `value` SHALL be numeric. `unit` SHALL name the unit, such as
`count`, `per-second`, `milliseconds`, or `ratio`.

---

# Required Fields

A Metrics object SHALL define `metrics_id`, `assessment_id`, `task_id`, `schema_version`,
`scope.capability`, and at least one `measurements` entry with `name`, `value`, and `unit`.

---

# Validation Rules

- `metrics_id` SHALL be unique within an assessment.
- Every measurement `value` SHALL be numeric and SHALL carry a `unit`.
- Measurements SHALL NOT encode interpretation, severity, or risk.
- Unknown optional fields SHALL be ignored for forward compatibility.

---

# Relationships

- A Metrics object MAY accompany [Artifacts](artifact.md) and
  [Observations](observation.md) produced in the same execution.
- A Metrics object SHALL NOT reference [Findings](finding.md) or [Risk](risk.md);
  interpretation belongs to domain capabilities.

---

# Example Object

```yaml
metrics_id: metrics-9001
assessment_id: assessment-2024-014
task_id: task-3120
schema_version: 1.0.0
scope:
  capability: fuzzing
  window:
    start: "2026-07-26T14:10:00Z"
    end: "2026-07-26T14:12:00Z"
measurements:
  - name: payloads.delivered
    value: 1840
    unit: count
  - name: requests.per_second
    value: 15.3
    unit: per-second
  - name: parameters.covered
    value: 0.82
    unit: ratio
```

---

# Extension Points

- Additional measurement `name` and `unit` values MAY be introduced.
- `scope` MAY be extended with additional context.
- Consumers SHALL ignore unknown optional fields.

---

# Versioning Notes

`schema_version` SHALL follow semantic versioning. Backward-compatible additions increment
the minor version. Unknown optional fields SHALL be ignored by consumers.
