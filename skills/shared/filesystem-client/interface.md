# Filesystem Client Interface

**File:** `skills/shared/filesystem-client/interface.md`

**Version:** 1.0.0

---

# Purpose

The Filesystem Client Interface defines the canonical contract through which
platform components access files.

The interface standardizes operation requests, path confinement, read and write
operations, and result propagation while remaining independent of any backend
implementation.

All consumers SHALL perform filesystem access exclusively through this interface.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- Backend Independent
- Versioned
- Observable
- Backward Compatible
- Confinement-First

---

# Relationship

```
Master Agent

↓

Domain Skill

↓

Filesystem Client Interface

↓

Filesystem Client Shared Skill

↓

Filesystem Adapter
```

The interface SHALL NOT expose or depend on adapter internals.

---

# Interface Overview

```
Metadata

↓

Root Reference

↓

Operation

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

# Root Reference

Every invocation SHALL define

```yaml
root_id:

path:
```

`root_id` SHALL reference a configured root.

`path` SHALL be a relative path resolved and confined within the root.

---

# Operation

Every invocation SHALL define

```yaml
kind:

content_ref:

options:
```

`kind` SHALL be one of `read`, `write`, `append`, `list`, `stat`, or `delete`.

`content_ref` SHALL reference content to write for `write` and `append`.

`options` MAY include `follow_symlinks`, `max_bytes`, and `max_depth`.

`write`, `append`, and `delete` SHALL be authorized as intrusive.

---

# Governance References

Every invocation MAY reference

```yaml
rate_limit_policy_id:

retry_policy_id:

credential_ref:
```

`credential_ref` SHALL reference a credential for remote backends resolved by the
[Authentication](../authentication/README.md) package.

The interface SHALL NOT accept inline secrets.

---

# Execution Context

The Filesystem Client Shared Skill SHALL receive read-only context.

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

content_ref:

entries:

metadata:

error:

evidence:
```

`outcome` SHALL be one of

```
completed

traversal_rejected

not_found

rejected

timed_out
```

`content_ref` SHALL reference read content stored as an artifact for large files.

`entries` SHALL summarize directory entries for `list`.

`metadata` SHALL include size, permissions, and timestamps for `stat`.

Adapter-specific handles SHALL NOT be exposed.

---

# Evidence

The interface SHALL expose structured evidence.

Evidence MAY include

- Root and confined path
- Operation kind
- Size and entry counts
- Metadata

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain sensitive
contents.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the Filesystem Client error model](error-model.md).

A traversal or symlink-escape attempt SHALL map to a non-retryable rejection.

---

# Compatibility

The interface SHALL remain stable across backends and consumers.

Consumers SHALL require no modification when backends change.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL define

- Metadata
- Root Reference with a relative path
- Operation
- Execution Context
- Operation Result
- Error Handling
- Evidence

---

# Quality Requirements

The Filesystem Client Interface SHALL

✓ Remain backend independent

✓ Enforce confinement

✓ Bound sizes and depth

✓ Support structured errors

✓ Preserve evidence

✓ Protect sensitive contents

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Streaming read and write descriptors
- Change-watch subscriptions
- Extended attribute inspection

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Filesystem Client Interface provides a stable,
implementation-independent contract through which all platform components perform
confined, bounded, governed filesystem access across the Robust PenTest Platform.
