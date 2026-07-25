# Content Discovery Interface

**File:** `skills/discovery/content-discovery/interface.md`

**Version:** 1.0.0

---

# Purpose

The Content Discovery Interface defines the canonical contract through which the
platform invokes content discovery and receives canonical Assets, Observations,
and Findings.

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

Content Discovery Interface

↓

Content Discovery Skill

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
target:

wordlist_ref:

follow_links:

max_depth:
```

`target` SHALL be an in-scope web application base URL.

`wordlist_ref` SHALL reference a curated candidate-path list.

`follow_links` SHALL declare whether in-scope links are enumerated.

`max_depth` SHALL bound crawl depth.

---

# Policy References

Every invocation SHALL reference

```yaml
scope_id:

roe_id:
```

The skill SHALL consult the [Policy Engine](../../shared/policy-engine/README.md)
with these references before each request.

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

`assets` SHALL reference produced `endpoint` and `web-application`
[Assets](../../../schemas/asset.md).

`findings` SHALL reference produced [Findings](../../../schemas/finding.md).

`denied` SHALL indicate the Policy Engine denied the request.

---

# Produced Objects

Produced objects SHALL conform to their canonical schemas and SHALL be
referenced, not inlined.

Every produced Asset and Finding SHALL carry provenance to its Evidence.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the Content Discovery error model](error-model.md).

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
- Discovery Request with an in-scope target
- Policy References
- Execution Context
- Discovery Result
- Error Handling

---

# Quality Requirements

The Content Discovery Interface SHALL

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

- Rendered-content discovery descriptors
- Response-similarity clustering hints
- Parameter-discovery handoff to API Discovery

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Content Discovery Interface provides a stable,
implementation-independent contract through which the platform obtains canonical,
evidence-backed content Assets and exposure Findings, gated by the Policy Engine,
across the Robust PenTest Platform.
