# gRPC Client Examples

**File:** `skills/shared/grpc-client/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
gRPC Client Shared Skill in use.

Examples demonstrate unary and streaming calls, metadata, status mapping,
governance, evidence, and expected outputs.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Unary Call

An API-security skill invokes a unary method over TLS.

## Invocation

```yaml
metadata:
  request_id: req-9301
  assessment_id: asmt-42
  task_id: task-grpc-probe
  skill_id: api-grpc
authority: grpc.example.com:443
secure: true
service: shop.Catalog
method: GetItem
kind: unary
messages:
  - staging://grpc/get-item-request
deadline: 10s
```

## Result

```yaml
outcome: completed
status_code: OK
messages_received: 1
received_ref: artifact://grpc/req-9301-response
```

The call completes with `OK` and the response message is stored as an artifact.

---

# Example 2 — Server Streaming Bounded

A server-streaming call is bounded by message count.

## Call Options

```yaml
kind: server_streaming
max_messages: 100
deadline: 30s
```

## Result

```yaml
outcome: completed
status_code: OK
messages_received: 100
```

Streaming stops at the bound to prevent unbounded intake.

---

# Example 3 — Status Error

A method returns `PERMISSION_DENIED`.

## Result

```yaml
outcome: status_error
status_code: PERMISSION_DENIED
error:
  category: Status
  code: grpc_status_error
  status_code: PERMISSION_DENIED
  retryable: false
```

The status code is preserved for the domain skill to interpret; the transport
layer does not classify it as a finding.

---

# Example 4 — Retryable Status

An `UNAVAILABLE` status is retried.

## Configuration

```yaml
retryable_status_codes:
  - UNAVAILABLE
```

## Flow

```
Attempt 1 → acquire permit → UNAVAILABLE

↓ Retry (idempotent)

Attempt 2 → acquire permit → OK
```

Each attempt acquires its own rate permit.

---

# Example 5 — Deadline Exceeded

A long call exceeds its deadline.

## Result

```yaml
outcome: timed_out
error:
  category: Timeout
  code: deadline_exceeded
  retryable: false
```

The bounded deadline prevents indefinite calls.

---

# Example 6 — Metadata Without Secrets

A credential reference authenticates the call without inline secrets.

## Invocation

```yaml
credential_ref: cred-grpc-service
request_metadata:
  x-trace: enabled
```

The credential is resolved by the
[Authentication](../authentication/README.md) shared package; no secret appears
in metadata.

---

# Example 7 — Evidence Record

A single call produces the following evidence.

```yaml
evidence:
  type: grpc-call
  authority: grpc.example.com:443
  method: shop.Catalog/GetItem
  status_code: OK
  messages_sent: 1
  messages_received: 1
  duration_ms: 64
  decided_at: 2026-07-25T14:30:00Z
```

The evidence conforms to the canonical
[Evidence schema](../../../schemas/evidence.md), excludes secret payloads and
metadata, and supports auditing.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [HTTP Client](../http-client/README.md)
- [TLS Client](../tls-client/README.md)
