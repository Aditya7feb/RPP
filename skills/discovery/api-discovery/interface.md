# API Discovery Interface

**File:** `skills/discovery/api-discovery/interface.md`

**Version:** 1.0.0

---

# Purpose

The API Discovery Interface defines the canonical contract through which the
platform invokes API discovery and receives canonical Assets, Observations, and
Findings.

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

API Discovery Interface

↓

API Discovery Skill

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

definition_hints:

detect_graphql:

base_path_candidates_ref:
```

`target` SHALL be an in-scope application or API base URL.

`definition_hints` SHALL reference candidate specification paths.

`detect_graphql` SHALL declare whether GraphQL detection is performed.

`base_path_candidates_ref` SHALL reference candidate API base paths.

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

`assets` SHALL reference produced `api` and `endpoint`
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
[the API Discovery error model](error-model.md).

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

The API Discovery Interface SHALL

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

- gRPC and AsyncAPI definition descriptors
- Structured operation Assets from parsed specifications
- API version-diff requests

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant API Discovery Interface provides a stable,
implementation-independent contract through which the platform obtains canonical,
evidence-backed API Assets and API-exposure Findings, gated by the Policy Engine,
across the Robust PenTest Platform.
