# Cloud Storage Client Interface

**File:** `skills/shared/cloud-storage-client/interface.md`

**Version:** 1.0.0

---

# Purpose

The Cloud Storage Client Interface defines the canonical contract through which
platform components access object storage.

The interface standardizes object operations, scope confinement, encryption, and
result propagation while remaining independent of any provider implementation.

All consumers SHALL perform object-storage access exclusively through this
interface.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- Provider Independent
- Versioned
- Observable
- Backward Compatible
- Scope-Confined

---

# Relationship

```
Master Agent

↓

Cloud Domain Skill

↓

Cloud Storage Client Interface

↓

Cloud Storage Client Shared Skill

↓

Provider Adapter
```

The interface SHALL NOT expose or depend on adapter internals.

---

# Interface Overview

```
Metadata

↓

Scope Reference

↓

Operation

↓

Encryption

↓

Governance References

↓

Execution Context

↓

Operation Result

↓

Evidence

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

# Scope Reference

Every invocation SHALL define

```yaml
scope_id:

bucket:

key:

credential_ref:
```

`scope_id` SHALL reference an authorized bucket-and-prefix scope.

`key` SHALL be an object key confined within the scope prefix.

`credential_ref` SHALL reference a credential resolved by the
[Authentication](../authentication/README.md) package.

The interface SHALL NOT accept inline secrets.

---

# Operation

Every invocation SHALL define

```yaml
kind:

content_ref:

options:
```

`kind` SHALL be one of `list`, `read`, `write`, `stat`, `delete`, or `presign`.

`content_ref` SHALL reference content to write for `write`.

`options` MAY include `max_bytes`, `max_keys`, and `presign_ttl`.

`write`, `delete`, and policy-affecting operations SHALL be authorized as
intrusive.

---

# Encryption

Every write invocation SHALL define

```yaml
encryption:
```

`encryption` SHALL declare the required server-side encryption mode, or reference
a client-side key resolved through the
[Secrets Client](../secrets-client/README.md).

Where encryption is required and unavailable, the write SHALL fail.

---

# Governance References

Every invocation MAY reference

```yaml
rate_limit_policy_id:

retry_policy_id:
```

Referenced policies SHALL conform to their canonical schemas. Absent references
SHALL inherit configured defaults.

---

# Execution Context

The Cloud Storage Client Shared Skill SHALL receive read-only context.

```yaml
execution_id:

parent_span:

variables:
```

The interface SHALL treat context as read-only.

---

# Operation Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

objects:

content_ref:

access_metadata:

presigned_ref:

error:

evidence:
```

`outcome` SHALL be one of

```
completed

scope_rejected

encryption_required_unavailable

not_found

rejected

timed_out
```

`access_metadata` SHALL include public-access flags and encryption status as
data.

`presigned_ref`, when present, SHALL be treated as sensitive and SHALL NOT appear
in evidence.

Provider-specific handles SHALL NOT be exposed.

---

# Evidence

The interface SHALL expose structured evidence.

Evidence MAY include

- Bucket, prefix, and key
- Operation kind
- Object size and count
- Access metadata

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain object
contents or presigned references.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the Cloud Storage Client error model](error-model.md).

A scope violation SHALL map to a non-retryable rejection.

---

# Compatibility

The interface SHALL remain stable across providers and consumers.

Consumers SHALL require no modification when providers change.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL define

- Metadata
- Scope Reference with a confined key
- Operation
- Encryption for writes
- Execution Context
- Operation Result
- Error Handling
- Evidence

---

# Quality Requirements

The Cloud Storage Client Interface SHALL

✓ Remain provider independent

✓ Enforce scope confinement

✓ Enforce encryption where mandated

✓ Support structured errors

✓ Preserve evidence

✓ Protect contents and references

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Multipart and resumable transfer descriptors
- Versioned-object inspection
- Lifecycle-policy observation

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Cloud Storage Client Interface provides a stable,
implementation-independent contract through which all platform components perform
confined, encrypted, governed object-storage access across the Robust PenTest
Platform.
