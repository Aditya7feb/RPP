# TCP Client Examples

**File:** `skills/shared/tcp-client/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
TCP Client Shared Skill in use.

Examples demonstrate connection establishment, byte exchange, proxy routing,
governance, timeouts, evidence, and expected outputs.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Establishing A Bounded Connection

A port discovery skill establishes a bounded connection to check a service.

## Invocation

```yaml
metadata:
  request_id: req-8001
  assessment_id: asmt-42
  task_id: task-port-check
  skill_id: port-discovery
host: mail.example.com
port: 25
connect_timeout: 3s
deadline: 5s
```

## Result

```yaml
outcome: completed
bytes_received: 42
timing:
  connect_ms: 38
  first_byte_ms: 51
```

The connection succeeds and the service banner bytes are returned without
interpretation.

---

# Example 2 — Byte Exchange For A Higher-Level Client

The SMTP Client sends a greeting and reads the response through the TCP Client.

## Exchange Descriptor

```yaml
send: staging://smtp/ehlo-line
expect:
  strategy: read_until_close
  max_bytes: 65536
```

## Result

```yaml
outcome: completed
bytes_sent: 18
bytes_received: 220
received_ref: artifact://smtp/req-8002-response
```

The TCP Client moves bytes; SMTP semantics are handled by the
SMTP Client.

---

# Example 3 — Proxy Routing

A connection is routed through a SOCKS5 proxy.

## Governance References

```yaml
proxy_id: proxy-socks
```

## Result

```yaml
outcome: completed
evidence:
  routing:
    decision: proxied
    proxy_id: proxy-socks
```

The connection is tunneled through the [Proxy](../proxy/README.md) shared skill.

---

# Example 4 — Connection Refused With Retry

A transient connection failure is retried.

## Flow

```
Attempt 1 → acquire permit → connect_refused

↓ Retry decides to retry

Attempt 2 → acquire permit → completed
```

## Result

```yaml
outcome: completed
attempts: 2
```

Each attempt acquires its own rate permit, keeping traffic within the configured
rate.

---

# Example 5 — Timeout

A connection exceeds its deadline.

## Result

```yaml
outcome: timed_out
error:
  category: Timeout
  code: connect_timeout
  breached_bound: connect
  retryable: false
```

The bounded connection prevents indefinite blocking.

---

# Example 6 — Governance Blocks Direct Egress

Governance requires a proxy, but none applies to the destination.

## Result

```yaml
outcome: rejected
error:
  category: Governance
  code: direct_egress_blocked
  retryable: false
```

The connection is refused to preserve Rules of Engagement.

---

# Example 7 — Evidence Record

A single connection produces the following evidence.

```yaml
evidence:
  type: tcp-connection
  endpoint: mail.example.com:25
  outcome: completed
  bytes_sent: 18
  bytes_received: 220
  timing:
    connect_ms: 38
  decided_at: 2026-07-25T13:00:00Z
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
- [Proxy](../proxy/README.md)
- SMTP Client
