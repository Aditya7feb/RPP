# UDP Client Examples

**File:** `skills/shared/udp-client/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
UDP Client Shared Skill in use.

Examples demonstrate datagram exchange, no-response handling, amplification
protection, idempotent retry, evidence, and expected outputs.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Request And Response

A service discovery skill sends a probe and awaits a response.

## Invocation

```yaml
metadata:
  request_id: req-9101
  assessment_id: asmt-42
  task_id: task-udp-probe
  skill_id: service-discovery
host: ntp.example.com
port: 123
datagram:
  payload_ref: staging://udp/ntp-request
  idempotent: true
  expect_response: true
response_window: 2s
```

## Result

```yaml
outcome: responded
response_bytes: 48
latency: 41ms
response_ref: artifact://udp/req-9101-response
```

The response is correlated to the request within the window.

---

# Example 2 — No Response Is Normal

A probe to a filtered UDP port yields no response.

## Result

```yaml
outcome: no_response
```

`no_response` is a normal outcome, not an error. The consuming skill decides its
significance.

---

# Example 3 — Amplification Protection

A datagram whose expected response ratio is excessive is refused.

## Configuration

```yaml
amplification:
  max_response_ratio: 4
  enforce: true
```

## Result When Ratio Exceeded

```yaml
outcome: rejected
error:
  category: Governance
  code: amplification_exceeded
  retryable: false
```

The exchange is refused to prevent amplification abuse.

---

# Example 4 — Fire-And-Forget

A datagram is sent without awaiting a response.

## Invocation

```yaml
datagram:
  payload_ref: staging://udp/notify
  idempotent: true
  expect_response: false
```

## Result

```yaml
outcome: sent
```

The datagram is sent and no response is awaited.

---

# Example 5 — Idempotent Retry

An idempotent exchange is retried after a send failure.

## Flow

```
Attempt 1 → acquire permit → send_failed

↓ Retry (idempotent only)

Attempt 2 → acquire permit → responded
```

Non-idempotent exchanges would NOT be retried.

---

# Example 6 — Deadline Exceeded

A total deadline is exceeded while awaiting a response.

## Result

```yaml
outcome: timed_out
error:
  category: Timeout
  code: deadline_exceeded
  retryable: false
```

The bounded exchange prevents indefinite waiting.

---

# Example 7 — Evidence Record

A single exchange produces the following evidence.

```yaml
evidence:
  type: udp-exchange
  endpoint: ntp.example.com:123
  outcome: responded
  sent_bytes: 48
  response_bytes: 48
  latency: 41ms
  decided_at: 2026-07-25T13:30:00Z
```

The evidence conforms to the canonical
[Evidence schema](../../../schemas/evidence.md), excludes secret payloads, and
supports auditing.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [TCP Client](../tcp-client/README.md)
