# Virtual Host Discovery Interface

**File:** `skills/discovery/virtual-host-discovery/interface.md`

**Version:** 1.0.0

---

# Purpose

The Virtual Host Discovery Interface defines the canonical contract through which
the platform invokes virtual host discovery and receives canonical Assets,
Observations, and Findings.

The interface standardizes the discovery request, the produced domain objects, and
result propagation while remaining independent of any HTTP implementation.

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

Virtual Host Discovery Interface

↓

Virtual Host Discovery Skill

↓

Policy Engine + HTTP Client + Evidence
```

The interface SHALL NOT expose or depend on HTTP implementation internals.

---

# Interface Overview

```
Metadata

↓

Discovery Request

↓

Policy References

↓

Execution Context

↓

Discovery Result

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

# Discovery Request

Every invocation SHALL define

```yaml
target_address:

host_candidates_ref:

base_scheme:
```

`target_address` SHALL be an in-scope address.

`host_candidates_ref` SHALL reference a candidate host-name list.

`base_scheme` SHALL declare `http`, `https`, or both.

---

# Policy References

Every invocation SHALL reference

```yaml
scope_id:

roe_id:
```

The skill SHALL consult the [Policy Engine](../../shared/policy-engine/README.md)
with these references before each probe.

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

# Discovery Result

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

`assets` SHALL reference produced `web-application`
[Assets](../../../schemas/asset.md) for distinct virtual hosts.

`findings` SHALL reference produced [Findings](../../../schemas/finding.md).

`denied` SHALL indicate the Policy Engine denied the probe.

---

# Produced Objects

Produced objects SHALL conform to their canonical schemas and SHALL be
referenced, not inlined.

Every produced Asset and Finding SHALL carry provenance to its Evidence.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the Virtual Host Discovery error model](error-model.md).

A Policy Engine denial SHALL produce a `denied` outcome, not an error retry.

---

# Compatibility

The interface SHALL remain stable across HTTP implementations and consumers.

Consumers SHALL require no modification when the HTTP Client implementation
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
- Discovery Request with an in-scope address
- Policy References
- Execution Context
- Discovery Result
- Error Handling

---

# Quality Requirements

The Virtual Host Discovery Interface SHALL

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

- Response-similarity clustering hints
- TLS SNI correlation descriptors
- Wildcard-response filtering directives

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Virtual Host Discovery Interface provides a stable,
implementation-independent contract through which the platform obtains canonical,
evidence-backed virtual host Assets and hidden-host Findings, gated by the Policy
Engine, across the Robust PenTest Platform.
