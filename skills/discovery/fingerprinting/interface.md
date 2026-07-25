# Fingerprinting Interface

**File:** `skills/discovery/fingerprinting/interface.md`

**Version:** 1.0.0

---

# Purpose

The Fingerprinting Interface defines the canonical contract through which the
platform invokes fingerprinting and receives canonical Technologies, Assets,
Observations, and Findings.

The interface standardizes the fingerprint request, the produced domain objects,
and result propagation while remaining independent of any transport
implementation.

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

Fingerprinting Interface

↓

Fingerprinting Skill

↓

Policy Engine + HTTP Client + TLS Client + Evidence
```

The interface SHALL NOT expose or depend on transport implementation internals.

---

# Interface Overview

```
Metadata

↓

Fingerprint Request

↓

Policy References

↓

Execution Context

↓

Fingerprint Result

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

# Fingerprint Request

Every invocation SHALL define

```yaml
target:

asset_id:

signals:

active:
```

`target` SHALL be an in-scope Asset endpoint.

`asset_id` MAY reference the fingerprinted Asset.

`signals` SHALL declare the signal sources to consult.

`active` SHALL declare whether active probing is permitted, subject to policy.

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

# Fingerprint Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

technologies:

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

`technologies` SHALL reference produced
[Technology](../../../schemas/technology.md) records with confidence grades.

`assets` and `relationships` SHALL reference produced Assets and relationships.

`findings` SHALL reference produced [Findings](../../../schemas/finding.md).

`denied` SHALL indicate the Policy Engine denied the action.

---

# Produced Objects

Produced objects SHALL conform to their canonical schemas and SHALL be
referenced, not inlined.

Every produced object SHALL carry provenance to its Evidence and a confidence
grade where applicable.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the Fingerprinting error model](error-model.md).

A Policy Engine denial SHALL produce a `denied` outcome, not an error retry.

---

# Compatibility

The interface SHALL remain stable across transport implementations and consumers.

Consumers SHALL require no modification when the transport implementation changes.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL define

- Metadata
- Fingerprint Request with an in-scope target
- Policy References
- Execution Context
- Fingerprint Result
- Error Handling

---

# Quality Requirements

The Fingerprinting Interface SHALL

✓ Remain implementation independent

✓ Produce canonical Technology and domain objects

✓ Enforce policy gating

✓ Grade identification confidence

✓ Support structured errors

✓ Preserve evidence provenance

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Technology-to-vulnerability mapping descriptors
- Favicon and asset-hash correlation hints
- Behavioral fingerprint requests

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Fingerprinting Interface provides a stable,
implementation-independent contract through which the platform obtains canonical,
evidence-backed Technology identifications and technology-exposure Findings, gated
by the Policy Engine, across the Robust PenTest Platform.
