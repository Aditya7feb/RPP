# TCP Client Interface

**File:** `skills/shared/tcp-client/interface.md`

**Version:** 1.0.0

---

# Purpose

The TCP Client Interface defines the canonical contract through which platform
components establish TCP connections and exchange bytes.

The interface standardizes connection requests, byte exchange, governance, and
result propagation while remaining independent of any transport implementation.

All consumers SHALL perform raw TCP transport exclusively through this interface.

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

Higher-Level Client or Domain Skill

↓

TCP Client Interface

↓

TCP Client Shared Skill

↓

Transport Adapter
```

The interface SHALL NOT expose or depend on adapter internals.

---

# Interface Overview

```
Metadata

↓

Endpoint

↓

Governance References

↓

Exchange Options

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

# Endpoint

Every invocation SHALL define

```yaml
host:

port:

address_family:
```

`host` SHALL be a hostname or address.

`port` SHALL be an integer from `1` through `65535`.

`address_family` MAY be `ipv4`, `ipv6`, or `any`.

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

# Exchange Options

The caller MAY specify

```yaml
connect_timeout:

read_timeout:

write_timeout:

deadline:

max_bytes:
```

`deadline` SHALL bound the total operation.

`max_bytes` SHALL bound the number of bytes read to prevent unbounded intake.

---

# Execution Context

The TCP Client Shared Skill SHALL receive read-only context.

```yaml
execution_id:

parent_span:

variables:
```

The interface SHALL treat context as read-only.

---

# Byte Exchange

The caller SHALL drive byte exchange through a normalized exchange descriptor.

```yaml
send:

expect:
```

`send` SHALL be the bytes to write, provided by reference for large payloads.

`expect` MAY declare a read strategy, such as a byte count or a bounded read
until close.

The interface SHALL NOT interpret payload contents.

---

# Connection Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

bytes_sent:

bytes_received:

received_ref:

timing:

error:

evidence:
```

`outcome` SHALL be one of

```
completed

connect_failed

timed_out

reset

rejected
```

`received_ref` SHALL reference received bytes stored as an artifact rather than
inlined for large payloads.

Adapter-specific socket objects SHALL NOT be exposed.

---

# Evidence

The interface SHALL expose structured evidence.

Evidence MAY include

- Endpoint
- Connection outcome
- Timing
- Byte counts
- Proxy routing decision

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain secret
payloads.

---

# Metrics

Execution metrics MAY include

```yaml
connect_latency:

bytes_sent:

bytes_received:

attempts:
```

Metrics SHOULD support observability.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the TCP Client error model](error-model.md).

Timeouts SHALL produce canonical timeout errors bounded by the supplied
deadlines.

---

# Compatibility

The interface SHALL remain stable across transport adapters and higher-level
consumers.

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
- Endpoint with a valid port
- Execution Context
- Bounded Exchange Options
- Connection Result
- Error Handling
- Evidence

---

# Quality Requirements

The TCP Client Interface SHALL

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

- Pooled connection handles
- Streaming exchange notifications
- Socket-option descriptors

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant TCP Client Interface provides a stable, implementation-independent
contract through which all platform components perform bounded, governed TCP
transport across the Robust PenTest Platform.
