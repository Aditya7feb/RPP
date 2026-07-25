# Proxy Interface

**File:** `skills/shared/proxy/interface.md`

**Version:** 1.0.0

---

# Purpose

The Proxy Interface defines the canonical contract through which platform
components route outbound operations through intermediaries.

The interface standardizes proxy selection, bypass evaluation, tunnel
establishment, and result propagation while remaining independent of any
operation implementation.

All consumers SHALL route outbound operations exclusively through this
interface.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- Operation Independent
- Versioned
- Observable
- Backward Compatible
- Deterministic

---

# Relationship

```
Master Agent

↓

Workflow

↓

Shared Package or Domain Skill

↓

Proxy Interface

↓

Proxy Shared Skill

↓

Caller-Provided Operation
```

The operation is supplied by the caller as an execution callback bound to the
routed channel. The interface SHALL NOT expose or depend on operation internals.

---

# Interface Overview

```
Metadata

↓

Destination

↓

Operation Reference

↓

Proxy Configuration

↓

Execution Options

↓

Execution Context

↓

Routing Result

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

# Destination

Every invocation SHALL define

```yaml
scheme:

host:

port:
```

The destination SHALL be used to evaluate selection and bypass rules.

---

# Operation Reference

Every invocation SHALL define

```yaml
operation:
```

`operation` SHALL be a caller-provided execution callback that performs a single
operation over the routed channel and returns a normalized outcome.

---

# Proxy Configuration

Every invocation SHALL reference configuration.

```yaml
proxy_id:
```

`proxy_id` SHALL reference a
[Proxy Configuration](../../../schemas/proxy-configuration.md), or the invocation
MAY reference a proxy set from which the applicable proxy is selected.

An invocation MAY supply an inline configuration override that conforms to the
Proxy Configuration schema. Overrides SHALL be validated before use.

---

# Execution Options

The caller MAY specify

```yaml
allow_direct_fallback:

capture_evidence:

emit_events:
```

`allow_direct_fallback` SHALL be a boolean gating direct fallback and SHALL be
honored only where Rules of Engagement permit direct egress.

These options influence execution without changing the interface.

---

# Execution Context

The Proxy Shared Skill SHALL receive read-only context.

```yaml
execution_id:

parent_span:

variables:
```

The interface SHALL treat context as read-only.

---

# Attempt Outcome

The caller-provided operation SHALL return a normalized outcome.

```yaml
success:

result:

error:
```

`success` SHALL be a boolean.

`error` SHALL conform to the canonical error structure when `success` is
`false`.

---

# Routing Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

result:

error:

routing:

evidence:
```

`outcome` SHALL be one of

```
executed

bypassed

proxy_unreachable

blocked
```

Transport-specific tunnel objects SHALL NOT be exposed.

---

## Routing Record

Each routing record SHALL include

```yaml
decision:

proxy_id:

destination:

interception:

decided_at:
```

`decision` SHALL be one of `proxied`, `direct`, or `direct_fallback`.

`interception` SHALL indicate whether TLS interception was declared for the
selected proxy.

---

# Evidence

The interface SHALL expose structured evidence.

Evidence MAY include

- Proxy reference
- Destination
- Routing decision
- Interception flag

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain proxy
credentials.

---

# Metrics

Execution metrics MAY include

```yaml
proxied:

bypassed:

direct_fallbacks:

tunnel_setup_time:
```

Metrics SHOULD support observability.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the Proxy error model](error-model.md).

When a proxy is unreachable and fallback is not permitted, the interface SHALL
propagate a canonical connection error.

---

# Compatibility

The interface SHALL remain stable across operation types.

```
HTTP Request Operation

↓

Same Interface

↓

TLS Handshake Operation

↓

Same Interface

↓

DNS Query Operation

↓

Same Interface
```

Consumers SHALL require no modification when operation types change.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL define

- Metadata
- Destination
- Operation Reference
- Proxy Configuration
- Execution Context
- Routing Result
- Error Handling
- Evidence

---

# Quality Requirements

The Proxy Interface SHALL

✓ Remain operation independent

✓ Produce normalized results

✓ Support structured errors

✓ Preserve execution context

✓ Preserve evidence

✓ Protect credentials

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Proxy chain descriptors
- Health-aware proxy pool references
- Dynamic selection rule sets

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Proxy Interface provides a stable, implementation-independent
contract through which all platform components route outbound operations.

It enables interchangeable operations to benefit from consistent, auditable, and
secure egress control across the Robust PenTest Platform.
