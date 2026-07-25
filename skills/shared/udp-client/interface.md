# UDP Client Interface

**File:** `skills/shared/udp-client/interface.md`

**Version:** 1.0.0

---

# Purpose

The UDP Client Interface defines the canonical contract through which platform
components exchange UDP datagrams.

The interface standardizes datagram requests, response correlation, governance,
and result propagation while remaining independent of any transport
implementation.

All consumers SHALL perform UDP transport exclusively through this interface.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- Transport Independent
- Versioned
- Observable
- Backward Compatible
- Explicit About Unreliability

---

# Relationship

```
Master Agent

↓

Domain Skill

↓

UDP Client Interface

↓

UDP Client Shared Skill

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

Datagram

↓

Governance References

↓

Exchange Options

↓

Execution Context

↓

Exchange Result

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

`port` SHALL be an integer from `1` through `65535`.

---

# Datagram

Every invocation SHALL define

```yaml
payload_ref:

idempotent:

expect_response:
```

`payload_ref` SHALL reference the datagram payload.

`idempotent` SHALL declare whether the exchange is safe to repeat. Retries SHALL
occur only when `idempotent` is `true`.

`expect_response` SHALL declare whether a response is awaited.

The interface SHALL NOT interpret payload contents.

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
response_window:

deadline:

max_response_bytes:
```

`response_window` SHALL bound how long a response is awaited.

`max_response_bytes` SHALL bound response intake.

---

# Execution Context

The UDP Client Shared Skill SHALL receive read-only context.

```yaml
execution_id:

parent_span:

variables:
```

The interface SHALL treat context as read-only.

---

# Exchange Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

response_ref:

response_bytes:

latency:

error:

evidence:
```

`outcome` SHALL be one of

```
responded

no_response

sent

rejected

timed_out
```

`sent` SHALL apply when `expect_response` is `false`.

`response_ref` SHALL reference response bytes stored as an artifact for large
responses.

Adapter-specific socket objects SHALL NOT be exposed.

---

# Evidence

The interface SHALL expose structured evidence.

Evidence MAY include

- Endpoint
- Sent size
- Response outcome and size
- Latency

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain secret
payloads.

---

# Metrics

Execution metrics MAY include

```yaml
sent:

responded:

no_response:

latency:
```

Metrics SHOULD support observability.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the UDP Client error model](error-model.md).

A `no_response` outcome SHALL NOT, by itself, be an error.

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
- Endpoint with a valid port
- Datagram with an idempotency declaration
- Execution Context
- Bounded Exchange Options
- Exchange Result
- Error Handling
- Evidence

---

# Quality Requirements

The UDP Client Interface SHALL

✓ Remain transport independent

✓ Make unreliability explicit

✓ Enforce bounds

✓ Support structured errors

✓ Preserve evidence

✓ Support observability

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Multi-response collection
- Multicast descriptors
- Streaming response notifications

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant UDP Client Interface provides a stable, implementation-independent
contract through which all platform components perform bounded, governed UDP
transport across the Robust PenTest Platform.
