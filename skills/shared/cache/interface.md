# Cache Interface

**File:** `skills/shared/cache/interface.md`

**Version:** 1.0.0

---

# Purpose

The Cache Interface defines the canonical contract through which platform
components store and reuse deterministic operation results.

The interface standardizes key derivation, lookup, revalidation, storage, and
result propagation while remaining independent of any operation implementation.

All consumers SHALL cache results exclusively through this interface.

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

Cache Interface

↓

Cache Shared Skill

↓

Caller-Provided Producer
```

On a miss, the value is produced by the caller through a producer callback. The
interface SHALL NOT expose or depend on producer internals.

---

# Interface Overview

```
Metadata

↓

Key Request

↓

Producer Reference

↓

Cache Options

↓

Execution Context

↓

Cache Result

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

# Key Request

Every invocation SHALL define the key components.

```yaml
namespace:

operation:

parameters:

scope:
```

`namespace` and `operation` SHALL identify the logical cache and operation.

`parameters` SHALL be the normalized operation parameters from which the
`parameters_digest` is derived. `parameters` SHALL NOT contain secret material.

`scope` SHALL be one of `assessment`, `session`, or `global`.

---

# Producer Reference

Every invocation SHALL define

```yaml
producer:

cacheable:

ttl:
```

`producer` SHALL be a caller-provided callback that produces the value on a
miss and returns a normalized outcome.

`cacheable` SHALL be a boolean declaring whether the produced value MAY be
stored.

`ttl` SHALL be the freshness duration for a newly stored entry.

---

# Cache Options

The caller MAY specify

```yaml
allow_stale:

revalidate:

capture_evidence:

emit_events:
```

`allow_stale` SHALL gate stale-while-revalidate serving.

`revalidate` SHALL request conditional revalidation using entry validators.

These options influence execution without changing the interface.

---

# Execution Context

The Cache Shared Skill SHALL receive read-only context.

```yaml
execution_id:

parent_span:

variables:
```

The interface SHALL treat context as read-only.

---

# Producer Outcome

The caller-provided producer SHALL return a normalized outcome.

```yaml
success:

value:

validators:

error:
```

`success` SHALL be a boolean.

`value` SHALL be present when `success` is `true`.

`validators` MAY carry freshness validators for future revalidation.

`error` SHALL conform to the canonical error structure when `success` is
`false`.

---

# Cache Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

value:

entry_ref:

freshness:

error:

evidence:
```

`outcome` SHALL be one of

```
hit

stale_hit

miss_stored

miss_uncached

revalidated

error
```

`entry_ref`, when present, SHALL reference the stored
[Cache Entry](../../../schemas/cache-entry.md).

Storage-specific objects SHALL NOT be exposed.

---

# Evidence

The interface SHALL expose structured evidence.

Evidence MAY include

- Key reference
- Lookup decision
- Provenance
- Freshness

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain cached
secrets.

---

# Metrics

Execution metrics MAY include

```yaml
hits:

misses:

stale_serves:

revalidations:

stores:

evictions:
```

Metrics SHOULD support observability.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the Cache error model](error-model.md).

A producer failure on a miss SHALL propagate the producer error.

---

# Compatibility

The interface SHALL remain stable across operation types.

```
DNS Resolve Result

↓

Same Interface

↓

TLS Metadata Result

↓

Same Interface

↓

HTTP GET Result

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
- Key Request with non-secret parameters
- Producer Reference
- Scope
- Execution Context
- Cache Result
- Error Handling
- Evidence

---

# Quality Requirements

The Cache Interface SHALL

✓ Remain operation independent

✓ Produce normalized results

✓ Support structured errors

✓ Preserve execution context

✓ Preserve evidence

✓ Exclude secrets

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Batch lookup requests
- Negative-cache descriptors
- Content-addressed value references
- Streaming revalidation notifications

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Cache Interface provides a stable, implementation-independent
contract through which all platform components store and reuse deterministic
results.

It enables interchangeable operations to benefit from consistent, scope-aware,
and observable caching across the Robust PenTest Platform.
