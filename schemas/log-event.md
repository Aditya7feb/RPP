# Log Event Schema

**File:** `schemas/log-event.md`

**Version:** 1.0.0

---

# Purpose

The Log Event Schema defines the canonical, implementation-independent
representation of a structured log record within the Robust PenTest Platform
(RPP).

A log event describes a single observable moment in execution: its severity,
message, source, correlation identifiers, and structured attributes. It is
produced through the [Logging](../skills/shared/logging/README.md) shared
package and consumed by observability, auditing, and reporting components.

A Log Event object represents an observability record only. It SHALL NOT contain
security interpretation as a finding, and it SHALL NOT contain secrets.

---

# Design Principles

A Log Event SHALL be

- Structured
- Correlatable
- Severity graded
- Transport independent
- Reusable across packages
- Free of embedded secrets

---

# Identity

Every Log Event SHALL contain

```yaml
event_id:

schema_version:

timestamp:
```

`event_id` SHALL be unique within a log stream.

`schema_version` SHALL be `1.0.0`.

`timestamp` SHALL be an absolute time in UTC.

---

# Severity

Every Log Event SHALL contain

```yaml
severity:
```

`severity` SHALL be one of

```
trace

debug

info

warn

error

fatal
```

`severity` SHALL reflect operational significance, not security risk. Security
risk is expressed by the [Finding schema](finding.md), not by log severity.

---

# Message

Every Log Event SHALL contain

```yaml
message:
```

`message` SHALL be a concise, human-readable description of the event.

`message` SHALL NOT contain secret material.

---

# Source

Every Log Event SHALL contain

```yaml
source:
```

`source` SHALL contain

```yaml
component:

layer:

operation:
```

`component` SHALL identify the emitting package, such as `http-client`.

`layer` SHALL identify the architectural layer, such as `shared` or `discovery`.

`operation` SHALL identify the operation in progress.

---

# Correlation

Every Log Event SHALL contain

```yaml
correlation:
```

`correlation` SHALL contain

```yaml
assessment_id:

task_id:

request_id:

execution_id:

span_id:
```

Correlation identifiers link log events to the originating assessment, task, and
execution span, enabling end-to-end tracing.

A Log Event MAY contain

```yaml
parent_span_id:
```

`parent_span_id` SHALL reference the enclosing span where one exists.

---

# Attributes

A Log Event MAY contain

```yaml
attributes:
```

`attributes` SHALL be a map of namespaced, structured key-value pairs providing
additional context.

`attributes` SHALL NOT contain secrets. Sensitive values SHALL be redacted or
referenced indirectly.

---

# Category

Every Log Event SHALL contain

```yaml
category:
```

`category` SHALL be one of

```
lifecycle

execution

network

security_event

audit

diagnostic
```

`security_event` denotes a security-relevant observation for audit purposes. It
SHALL NOT be treated as a confirmed [Finding](finding.md).

---

# Redaction

Every Log Event SHALL contain

```yaml
redaction:
```

`redaction` SHALL contain

```yaml
applied:

fields:
```

`applied` SHALL be a boolean indicating whether redaction was performed.

`fields` SHALL list attribute keys that were redacted.

Redaction SHALL occur before a Log Event is emitted.

---

# Evidence Linkage

A Log Event MAY contain

```yaml
evidence_ref:
```

`evidence_ref` SHALL reference related evidence conforming to the
[Evidence schema](evidence.md) where an event corresponds to captured evidence.

---

# Extensions

A Log Event MAY contain

```yaml
extensions:
```

`extensions` SHALL contain namespaced metadata.

`extensions` SHALL NOT contain secrets.

---

# Required Fields

A valid Log Event object SHALL contain

- `event_id`
- `schema_version`
- `timestamp`
- `severity`
- `message`
- `source.component`
- `source.layer`
- `correlation.assessment_id`
- `category`
- `redaction.applied`

---

# Validation Rules

A valid Log Event object SHALL satisfy

- `severity` is one of the allowed severities
- `category` is one of the allowed categories
- `timestamp` is a valid UTC time
- No secret material appears in `message`, `attributes`, or `extensions`
- `redaction.fields` is present when `redaction.applied` is `true`
- `evidence_ref`, when present, references a valid evidence object

---

# Relationships

```
Log Event

├── produced by the Logging shared package
├── correlated to Assessment, Task, and Execution
├── optionally linked to Evidence
└── consumed by observability, audit, and reporting
```

A Log Event is produced by the
[Logging](../skills/shared/logging/README.md) shared package on behalf of any
component. Correlation identifiers reference the
[Assessment](assessment.md), [Task](task.md), and
[Execution State](execution-state.md). Security-relevant events support the
audit trail without replacing the [Finding schema](finding.md).

---

# Example Object

```yaml
event_id: log-000123
schema_version: 1.0.0
timestamp: 2026-07-25T12:00:00Z
severity: info
message: HTTP request completed
source:
  component: http-client
  layer: shared
  operation: send-request
correlation:
  assessment_id: asmt-42
  task_id: task-content-discovery
  request_id: req-4001
  execution_id: exec-0007
  span_id: span-0031
  parent_span_id: span-0030
category: network
attributes:
  method: GET
  status_code: 200
  duration_ms: 142
redaction:
  applied: true
  fields:
    - authorization
evidence_ref: evidence-http-4001
```

---

# Versioning Notes

The schema SHALL follow semantic versioning.

Minor versions MAY introduce optional fields such as additional categories or
correlation identifiers.

Major versions SHALL indicate breaking changes, such as renaming or removing a
required field.

Consumers SHOULD ignore unknown optional fields to preserve forward
compatibility.
