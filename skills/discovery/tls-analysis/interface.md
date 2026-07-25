# TLS Analysis Interface

**File:** `skills/discovery/tls-analysis/interface.md`

**Version:** 1.0.0

---

# Purpose

The TLS Analysis Interface defines the canonical contract through which the
platform invokes TLS analysis and receives canonical Assets, Observations, and
Findings.

The interface standardizes the analysis request, the produced domain objects, and
result propagation while remaining independent of any TLS implementation.

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

TLS Analysis Interface

↓

TLS Analysis Skill

↓

Policy Engine + TLS Client + Evidence
```

The interface SHALL NOT expose or depend on TLS implementation internals.

---

# Interface Overview

```
Metadata

↓

Analysis Request

↓

Policy References

↓

Execution Context

↓

Analysis Result

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

# Analysis Request

Every invocation SHALL define

```yaml
target:

service_asset_id:

checks:
```

`target` SHALL be an in-scope TLS service endpoint.

`service_asset_id` MAY reference the analyzed `service` Asset.

`checks` SHALL declare the analyses to perform, such as `protocols`, `ciphers`,
`certificate`, and `validation`.

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

# Analysis Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

assets:

relationships:

observations:

findings:

tls_summary:

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

`tls_summary` SHALL report negotiated protocols, ciphers, and validation outcomes
as data.

`assets` SHALL reference produced `certificate`
[Assets](../../../schemas/asset.md).

`findings` SHALL reference produced [Findings](../../../schemas/finding.md).

`denied` SHALL indicate the Policy Engine denied the action.

---

# Produced Objects

Produced objects SHALL conform to their canonical schemas and SHALL be
referenced, not inlined.

Every produced Asset and Finding SHALL carry provenance to its Evidence.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the TLS Analysis error model](error-model.md).

A Policy Engine denial SHALL produce a `denied` outcome, not an error retry.

---

# Compatibility

The interface SHALL remain stable across TLS implementations and consumers.

Consumers SHALL require no modification when the TLS Client implementation
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
- Analysis Request with an in-scope target
- Policy References
- Execution Context
- Analysis Result
- Error Handling

---

# Quality Requirements

The TLS Analysis Interface SHALL

✓ Remain implementation independent

✓ Produce canonical domain objects

✓ Enforce policy gating

✓ Honor interception boundaries

✓ Support structured errors

✓ Preserve evidence provenance

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Revocation-state descriptors
- Certificate transparency correlation
- Cipher-preference-order reports

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant TLS Analysis Interface provides a stable,
implementation-independent contract through which the platform obtains canonical,
evidence-backed certificate Assets and TLS-weakness Findings, gated by the Policy
Engine, across the Robust PenTest Platform.
