# WebSocket Client Examples

**File:** `skills/shared/websocket-client/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
WebSocket Client Shared Skill in use.

Examples demonstrate the handshake, secure connections, frame exchange,
subprotocol negotiation, closure, evidence, and expected outputs.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Secure Handshake And Message Exchange

An API-security skill connects to a secure WebSocket endpoint and exchanges
messages.

## Invocation

```yaml
metadata:
  request_id: req-9201
  assessment_id: asmt-42
  task_id: task-ws-probe
  skill_id: api-websocket
url: wss://app.example.com/socket
subprotocols:
  - json
send:
  - type: text
    payload_ref: staging://ws/hello
receive:
  strategy: frame_count
  count: 1
```

## Result

```yaml
outcome: completed
handshake_ref: httptx-ws-9201
negotiated_subprotocol: json
frames_sent: 1
frames_received: 1
close:
  code: 1000
  reason: normal
```

The handshake is preserved as an
[HTTP Transaction](../../../schemas/http-transaction.md); TLS is handled by the
[TLS Client](../tls-client/README.md).

---

# Example 2 — Handshake Rejected

The server rejects the upgrade with a non-101 response.

## Result

```yaml
outcome: handshake_failed
error:
  category: Handshake
  code: upgrade_rejected
  retryable: false
```

The canonical HTTP handshake error is propagated.

---

# Example 3 — Required Subprotocol Unavailable

The caller requires a subprotocol the server does not offer.

## Invocation

```yaml
subprotocols:
  - graphql-ws
require_subprotocol: true
```

## Result

```yaml
outcome: rejected
error:
  category: Negotiation
  code: subprotocol_unavailable
  retryable: false
```

The connection is closed because the required subprotocol was not negotiated.

---

# Example 4 — Message Bound Enforcement

A received message exceeds the configured bound.

## Configuration

```yaml
bounds:
  max_message_bytes: 1MB
```

## Result

```yaml
outcome: completed
error:
  category: Validation
  code: message_too_large
  retryable: false
```

Oversized messages are rejected rather than buffered without limit.

---

# Example 5 — Ping And Pong

The client responds to a server ping automatically.

## Flow

```
Server → ping

Client → pong (automatic)
```

Control frames are managed by the shared skill.

---

# Example 6 — Peer Close Is Normal

The peer closes the connection with a normal code.

## Result

```yaml
outcome: closed_by_peer
close:
  code: 1000
  reason: normal
```

A peer close is a normal terminal condition, not an error.

---

# Example 7 — Evidence Record

A single connection produces the following evidence.

```yaml
evidence:
  type: websocket-connection
  url: wss://app.example.com/socket
  handshake_ref: httptx-ws-9201
  negotiated_subprotocol: json
  frames_sent: 1
  frames_received: 1
  close_code: 1000
  duration_ms: 812
  decided_at: 2026-07-25T14:00:00Z
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
- [HTTP Client](../http-client/README.md)
- [TLS Client](../tls-client/README.md)
