# Logging Examples

**File:** `skills/shared/logging/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
Logging Shared Skill in use.

Examples demonstrate consumers, structured events, correlation, redaction,
gating, evidence linkage, and expected outputs.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Structured Network Event

The HTTP Client logs a completed request.

## Request

```yaml
severity: info
message: HTTP request completed
category: network
source:
  component: http-client
  layer: shared
  operation: send-request
attributes:
  method: GET
  status_code: 200
  duration_ms: 142
evidence_ref: evidence-http-4001
```

## Emitted Event

```yaml
outcome: emitted
event_id: log-000123
```

Correlation identifiers are injected automatically from execution context.

---

# Example 2 — Automatic Redaction

An authenticated request carries an authorization header that MUST NOT be
logged.

## Request

```yaml
severity: debug
message: Sending authenticated request
category: network
source:
  component: http-client
  layer: shared
  operation: send-request
attributes:
  method: POST
  authorization: "Bearer eyJhbGciOi..."
```

## Emitted Event

```yaml
outcome: emitted
event_id: log-000124
redaction:
  applied: true
  fields:
    - authorization
```

The secret value is redacted before the event reaches any sink.

---

# Example 3 — Severity Gating

A `trace` event is dropped when the configured level is `info`.

## Configuration

```yaml
logging:
  level: info
```

## Result

```yaml
outcome: dropped
```

The event is not routed to any sink.

---

# Example 4 — Security Event For Audit

A discovery skill records a security-relevant observation.

## Request

```yaml
severity: warn
message: Directory listing enabled
category: security_event
source:
  component: content-discovery
  layer: discovery
  operation: probe-directory
attributes:
  path: /backups/
evidence_ref: evidence-dir-9001
```

## Result

```yaml
outcome: emitted
event_id: log-000125
```

The `security_event` supports the audit trail but is not a confirmed
[Finding](../../../schemas/finding.md); findings are produced separately.

---

# Example 5 — Correlated Trace

Multiple events share correlation identifiers, enabling end-to-end tracing.

```
span-0030 (task-content-discovery)
  ├── log-000123 (send-request)
  ├── log-000124 (parse-response)
  └── log-000125 (probe-directory)
```

All events reference `assessment_id: asmt-42` and `task_id:
task-content-discovery`.

---

# Example 6 — Sink Failure Under fail_open

A sink is temporarily unavailable while `failure_mode` is `fail_open`.

## Result

```yaml
outcome: dropped
```

The caller operation proceeds unaffected; the failure is counted internally.
Under `fail_closed`, a required-sink failure would instead return a canonical
logging error.

---

# Example 7 — Log Event Object

A single emitted event conforms to the canonical schema.

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
category: network
attributes:
  method: GET
  status_code: 200
  duration_ms: 142
redaction:
  applied: false
  fields: []
evidence_ref: evidence-http-4001
```

The event conforms to the canonical
[Log Event schema](../../../schemas/log-event.md).

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Log Event Schema](../../../schemas/log-event.md)
- [Evidence](../evidence/README.md)
