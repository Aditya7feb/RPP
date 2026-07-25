# Subdomain Discovery Interface

**File:** `skills/discovery/subdomain-discovery/interface.md`

**Version:** 1.0.0

---

# Purpose

The Subdomain Discovery Interface defines the canonical contract through which the
platform invokes subdomain discovery and receives canonical Assets, Observations,
and Findings.

The interface standardizes the discovery request, the produced domain objects, and
result propagation while remaining independent of any DNS implementation.

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

Subdomain Discovery Interface

↓

Subdomain Discovery Skill

↓

Policy Engine + DNS Client + Evidence
```

The interface SHALL NOT expose or depend on DNS implementation internals.

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
apex_domain:

sources:

wordlist_ref:

active_resolution:
```

`apex_domain` SHALL be an in-scope apex domain.

`sources` SHALL declare passive sources.

`wordlist_ref` SHALL reference a candidate list.

`active_resolution` SHALL declare whether active resolution is enabled, subject to
policy.

---

# Policy References

Every invocation SHALL reference

```yaml
scope_id:

roe_id:
```

The skill SHALL consult the [Policy Engine](../../shared/policy-engine/README.md)
with these references before each active resolution.

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

`assets` SHALL reference produced `subdomain`
[Assets](../../../schemas/asset.md), with state `suspected` or `confirmed`.

`findings` SHALL reference produced [Findings](../../../schemas/finding.md).

`denied` SHALL indicate the Policy Engine denied active resolution.

---

# Produced Objects

Produced objects SHALL conform to their canonical schemas and SHALL be
referenced, not inlined.

Every produced Asset and Finding SHALL carry provenance to its Evidence.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the Subdomain Discovery error model](error-model.md).

A Policy Engine denial SHALL produce a `denied` outcome, not an error retry.

---

# Compatibility

The interface SHALL remain stable across DNS implementations and consumers.

Consumers SHALL require no modification when the DNS Client implementation changes.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL define

- Metadata
- Discovery Request with an in-scope apex domain
- Policy References
- Execution Context
- Discovery Result
- Error Handling

---

# Quality Requirements

The Subdomain Discovery Interface SHALL

✓ Remain implementation independent

✓ Produce canonical domain objects

✓ Enforce policy gating for active resolution

✓ Support structured errors

✓ Preserve evidence provenance

✓ Support observability

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Certificate-transparency source descriptors
- Permutation-generation hints
- Passive DNS correlation requests

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Subdomain Discovery Interface provides a stable,
implementation-independent contract through which the platform obtains canonical,
evidence-backed subdomain Assets and takeover Findings, gated by the Policy
Engine, across the Robust PenTest Platform.
