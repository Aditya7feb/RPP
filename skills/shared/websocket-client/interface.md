# WebSocket Client Interface

**File:** `skills/shared/websocket-client/interface.md`

**Version:** 1.0.0

---

# Purpose

The WebSocket Client Interface defines the canonical contract through which
platform components establish WebSocket connections and exchange frames.

The interface standardizes connection requests, frame exchange, negotiation, and
result propagation while remaining independent of any transport implementation.

All consumers SHALL perform WebSocket transport exclusively through this
interface.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- Transport Independent
- Versioned
- Observable
- Backward Compatible
- Bounded

---

# Relationship

```
Master Agent

↓

Domain Skill

↓

WebSocket Client Interface

↓

WebSocket Client Shared Skill

↓

HTTP Client + TLS Client + Transport Adapter
```

The interface SHALL NOT expose or depend on adapter internals.

---

# Interface Overview

```
Metadata

↓

Connection Request

↓

Negotiation

↓

Governance References

↓

Frame Exchange

↓

Execution Context

↓

Connection Result

↓

Evidence

↓

Metrics

↓

Errors
```

---

# Metadata

Every invocation SHALL include

```yaml
request_id:

assessment_id:

task_id:

skill_id:

timestamp:
```

Metadata enables tracing and auditing.

---

# Connection Request

Every invocation SHALL define

```yaml
url:

secure:

headers:

credential_ref:
```

`url` SHALL be a `ws` or `wss` URL.

`secure` SHALL be derived from the scheme and SHALL select TLS for `wss`.

`credential_ref` MAY reference a credential resolved by the
[Authentication](../authentication/README.md) shared package for the handshake.

The interface SHALL NOT accept inline secrets.

---

# Negotiation

The caller MAY specify

```yaml
subprotocols:

extensions:

require_subprotocol:
```

`subprotocols` SHALL be an ordered preference list.

`require_subprotocol` SHALL declare whether a specific subprotocol is mandatory.

---

# Governance References

Every invocation MAY reference

```yaml
rate_limit_policy_id:

retry_policy_id:

proxy_id:
```

Referenced policies SHALL conform to their canonical schemas. Absent references
SHALL inherit configured defaults.

---

# Frame Exchange

The caller SHALL drive frames through a normalized exchange descriptor.

```yaml
send:

receive:
```

`send` SHALL be an ordered sequence of frames, each declaring a type and a
payload reference.

`receive` SHALL declare a receive strategy, such as a frame count or a bounded
receive until close.

The interface SHALL NOT interpret payload contents.

---

# Execution Context

The WebSocket Client Shared Skill SHALL receive read-only context.

```yaml
execution_id:

parent_span:

variables:
```

The interface SHALL treat context as read-only.

---

# Connection Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

handshake_ref:

negotiated_subprotocol:

frames_sent:

frames_received:

received_ref:

close:

error:

evidence:
```

`outcome` SHALL be one of

```
completed

handshake_failed

closed_by_peer

timed_out

rejected
```

`handshake_ref` SHALL reference the handshake
[HTTP Transaction](../../../schemas/http-transaction.md).

`close` SHALL include the close code and reason.

Adapter-specific connection objects SHALL NOT be exposed.

---

# Evidence

The interface SHALL expose structured evidence.

Evidence MAY include

- Handshake transaction reference
- Negotiated subprotocol and extensions
- Frame counts and sizes
- Close code and reason

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain secret
payloads.

---

# Metrics

Execution metrics MAY include

```yaml
frames_sent:

frames_received:

bytes_exchanged:

duration:
```

Metrics SHOULD support observability.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the WebSocket Client error model](error-model.md).

A handshake rejection SHALL propagate the canonical HTTP handshake error.

---

# Compatibility

The interface SHALL remain stable across transport adapters and consumers.

Consumers SHALL require no modification when adapters change.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL define

- Metadata
- Connection Request with a valid `ws` or `wss` URL
- Execution Context
- Bounded Frame Exchange
- Connection Result
- Error Handling
- Evidence

---

# Quality Requirements

The WebSocket Client Interface SHALL

✓ Remain transport independent

✓ Produce normalized results

✓ Enforce bounds

✓ Support structured errors

✓ Preserve evidence

✓ Support observability

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Streaming frame notifications
- Multiplexed channel descriptors
- Flow-control directives

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant WebSocket Client Interface provides a stable,
implementation-independent contract through which all platform components
perform bounded, governed WebSocket transport across the Robust PenTest Platform.
