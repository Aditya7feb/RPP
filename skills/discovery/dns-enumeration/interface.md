# DNS Enumeration Interface

**File:** `skills/discovery/dns-enumeration/interface.md`

**Version:** 1.0.0

---

# Purpose

The DNS Enumeration Interface defines the canonical contract through which the
platform invokes DNS enumeration and receives canonical Assets, Observations,
and Findings.

The interface standardizes the enumeration request, the produced domain objects,
and result propagation while remaining independent of any DNS implementation.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- Implementation Independent
- Versioned
- Observable
- Backward Compatible
- Policy-Gated

---

# Relationship

```
Recon Agent

↓

DNS Enumeration Interface

↓

DNS Enumeration Skill

↓

Policy Engine + DNS Client + Evidence
```

The interface SHALL NOT expose or depend on DNS implementation internals.

---

# Interface Overview

```
Metadata

↓

Enumeration Request

↓

Policy References

↓

Execution Context

↓

Enumeration Result

↓

Produced Objects

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

# Enumeration Request

Every invocation SHALL define

```yaml
target:

record_types:

recursive:
```

`target` SHALL be an in-scope domain or host.

`record_types` SHALL enumerate the record classes to query.

`recursive` SHALL declare whether discovered names are further enumerated within
scope and bounds.

---

# Policy References

Every invocation SHALL reference

```yaml
scope_id:

roe_id:
```

The skill SHALL consult the [Policy Engine](../../shared/policy-engine/README.md)
with these references before each action.

---

# Execution Context

The skill SHALL receive read-only context.

```yaml
execution_id:

parent_span:

variables:
```

The interface SHALL treat context as read-only.

---

# Enumeration Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

assets:

relationships:

observations:

findings:

metrics:

error:
```

`outcome` SHALL be one of

```
completed

partial

denied

timed_out
```

`assets` SHALL reference produced [Assets](../../../schemas/asset.md).

`relationships` SHALL reference produced
[Asset Relationships](../../../schemas/asset-relationship.md).

`observations` SHALL reference produced
[Observations](../../../schemas/observation.md).

`findings` SHALL reference produced [Findings](../../../schemas/finding.md).

`denied` SHALL indicate the Policy Engine denied the action.

---

# Produced Objects

Produced objects SHALL conform to their canonical schemas and SHALL be
referenced, not inlined, so that the assessment owns a single copy of each.

Every produced Asset and Finding SHALL carry provenance to its Evidence.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the DNS Enumeration error model](error-model.md).

A Policy Engine denial SHALL produce a `denied` outcome, not an error retry.

---

# Compatibility

The interface SHALL remain stable across DNS implementations and consumers.

Consumers SHALL require no modification when the DNS Client implementation
changes.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL define

- Metadata
- Enumeration Request with an in-scope target
- Policy References
- Execution Context
- Enumeration Result
- Error Handling

---

# Quality Requirements

The DNS Enumeration Interface SHALL

✓ Remain implementation independent

✓ Produce canonical domain objects

✓ Enforce policy gating

✓ Support structured errors

✓ Preserve evidence provenance

✓ Support observability

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Passive DNS result descriptors
- DNSSEC validation-state reporting
- Reverse-DNS sweep requests

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant DNS Enumeration Interface provides a stable,
implementation-independent contract through which the platform obtains canonical,
evidence-backed DNS Assets and Findings, gated by the Policy Engine, across the
Robust PenTest Platform.
