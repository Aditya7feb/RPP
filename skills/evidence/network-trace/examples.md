# Network Trace Examples

**File:** `skills/evidence/network-trace/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Network Trace Capability.

---

# Example 1 — Bounded TCP Flow Capture

## Request

```yaml
trace:
  target: 93.184.216.34
  selection:
    protocols: [tcp]
    ports: [443]
  bounds:
    max_flows: 200
    max_duration: 60s
  redaction:
    redact_payloads: true
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
trace_result:
  target: 93.184.216.34
  artifact_ref: artifact-ev-9201
  flow_count: 143
  evidence_ref: evidence-ev-8201
  metrics_ref: metrics-ev-7201
  decision_summary:
    allow: 1
    denied: 0
```

The capability captures a bounded set of TCP flows as a `network-trace` Artifact and invokes the
shared Evidence lifecycle to promote it.

---

# Example 2 — Requires Approval

## Request

```yaml
trace:
  target: 10.0.0.5
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
trace_result:
  target: 10.0.0.5
  metrics_ref: metrics-ev-7202
  decision_summary:
    allow: 0
    awaiting_approval: 1
```

The Rules of Engagement require approval before capturing this host; the capability defers.

---

# Example 3 — Out Of Scope Rejected

## Request

```yaml
trace:
  target: 203.0.113.9
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
trace_result:
  target: 203.0.113.9
  decision_summary:
    denied: 1
```

The target is out of scope, so the capability rejects the capture.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
