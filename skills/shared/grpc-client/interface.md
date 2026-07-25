# gRPC Client Interface

**File:** `skills/shared/grpc-client/interface.md`

**Version:** 1.0.0

---

# Purpose

The gRPC Client Interface defines the canonical contract through which platform
components invoke gRPC methods.

The interface standardizes call requests, streaming, metadata, status mapping,
and result propagation while remaining independent of any transport
implementation.

All consumers SHALL perform gRPC transport exclusively through this interface.

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

gRPC Client Interface

↓

gRPC Client Shared Skill

↓

HTTP Client (HTTP/2) + TLS Client + Transport Adapter
```

The interface SHALL NOT expose or depend on adapter internals.

---

# Interface Overview

```
Metadata

↓

Call Target

↓

Method

↓

Request Messages

↓

Governance References

↓

Call Options

↓

Execution Context

↓

Call Result

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

# Call Target

Every invocation SHALL define

```yaml
authority:

secure:

credential_ref:
```

`authority` SHALL be the host and port of the gRPC server.

`secure` SHALL select TLS.

`credential_ref` MAY reference a credential resolved by the
[Authentication](../authentication/README.md) shared package.

---

# Method

Every invocation SHALL define

```yaml
service:

method:

kind:
```

`service` and `method` SHALL identify the fully qualified method.

`kind` SHALL be one of `unary`, `server_streaming`, `client_streaming`, or
`bidirectional_streaming`.

---

# Request Messages

Every invocation SHALL define

```yaml
messages:

request_metadata:
```

`messages` SHALL be one message for unary and client-initiated calls, or a
bounded sequence for client-streaming and bidirectional calls, each provided by
reference.

`request_metadata` SHALL NOT contain inline secrets.

The interface SHALL NOT interpret message contents.

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

# Call Options

The caller MAY specify

```yaml
deadline:

max_message_bytes:

max_messages:
```

`deadline` SHALL bound the total call.

`max_message_bytes` and `max_messages` SHALL bound message size and count.

---

# Execution Context

The gRPC Client Shared Skill SHALL receive read-only context.

```yaml
execution_id:

parent_span:

variables:
```

The interface SHALL treat context as read-only.

---

# Call Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

status_code:

messages_received:

received_ref:

response_metadata:

trailers:

error:

evidence:
```

`outcome` SHALL be one of

```
completed

status_error

timed_out

rejected
```

`status_code` SHALL be the gRPC status code.

`received_ref` SHALL reference received messages stored as artifacts for large
payloads.

Adapter-specific call objects SHALL NOT be exposed.

---

# Evidence

The interface SHALL expose structured evidence.

Evidence MAY include

- Method and authority
- Message counts and sizes
- Status and trailers
- Call duration

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain secret
payloads or metadata.

---

# Metrics

Execution metrics MAY include

```yaml
messages_sent:

messages_received:

bytes_exchanged:

duration:
```

Metrics SHOULD support observability.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the gRPC Client error model](error-model.md).

A non-`OK` status SHALL map to a canonical error preserving the status code.

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
- Call Target with a valid authority
- Method with a valid kind
- Bounded Request Messages
- Execution Context
- Call Result
- Error Handling
- Evidence

---

# Quality Requirements

The gRPC Client Interface SHALL

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

- Reflection-based method descriptors
- Compression directives
- Streaming progress notifications

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant gRPC Client Interface provides a stable, implementation-independent
contract through which all platform components perform bounded, governed gRPC
transport across the Robust PenTest Platform.
