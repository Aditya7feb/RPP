# Cloud Storage Client Examples

**File:** `skills/shared/cloud-storage-client/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
Cloud Storage Client Shared Skill in use.

Examples demonstrate scope confinement, listing, encryption enforcement,
access-metadata observation, evidence, and expected outputs.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Scoped Listing

A cloud asset-discovery skill lists objects within an authorized scope.

## Invocation

```yaml
metadata:
  request_id: req-10101
  assessment_id: asmt-42
  task_id: task-bucket-audit
  skill_id: cloud-asset-discovery
scope_id: target-public-audit
bucket: target-assets
key: public/
credential_ref: cred-cloud-audit
kind: list
options:
  max_keys: 5000
```

## Result

```yaml
outcome: completed
objects:
  - key: public/index.html
    size: 1284
  - key: public/logo.png
    size: 44210
access_metadata:
  bucket_public: true
  encryption: provider-managed
```

The public-access flag is reported as data; whether it is a misconfiguration is
determined by cloud domain skills.

---

# Example 2 — Scope Rejection

An object key outside the authorized scope is rejected.

## Invocation

```yaml
scope_id: target-public-audit
key: private/secrets.env
```

## Result

```yaml
outcome: scope_rejected
error:
  category: Scope
  code: scope_rejected
  scope_id: target-public-audit
  retryable: false
```

The confinement boundary prevents access outside the authorized prefix.

---

# Example 3 — Encryption Enforced On Write

A write without available server-side encryption is refused.

## Configuration

```yaml
encryption:
  require_server_side: true
```

## Result

```yaml
outcome: encryption_required_unavailable
error:
  category: Encryption
  code: encryption_required_unavailable
  retryable: false
```

The write fails rather than storing unencrypted data.

---

# Example 4 — Authorized Staging Write

An evidence-staging write occurs within a writable, encrypted scope.

## Configuration

```yaml
scopes:
  - scope_id: staging
    writable: true
execution:
  allow_write: true
encryption:
  require_server_side: true
```

## Result

```yaml
outcome: completed
access_metadata:
  encryption: provider-managed
```

The write succeeds within the confined, writable, encrypted staging scope.

---

# Example 5 — Read Bounded By Reference

A large object is read within bounds and stored by reference.

## Result

```yaml
outcome: completed
content_ref: artifact://cloud/req-10105-object
access_metadata:
  encryption: provider-managed
```

Large object contents are stored by reference, not inlined.

---

# Example 6 — Presign Blocked

A presigned reference is requested while disabled.

## Configuration

```yaml
presign:
  allow_presign: false
```

## Result

```yaml
outcome: rejected
error:
  category: Governance
  code: presign_blocked
  retryable: false
```

Presigned references are gated and bounded when permitted.

---

# Example 7 — Evidence Record

A single operation produces the following evidence.

```yaml
evidence:
  type: cloud-storage-operation
  scope_id: target-public-audit
  bucket: target-assets
  prefix: public/
  kind: list
  object_count: 2
  bucket_public: true
  encryption: provider-managed
  decided_at: 2026-07-25T18:00:00Z
```

The evidence conforms to the canonical
[Evidence schema](../../../schemas/evidence.md), excludes object contents and
presigned references, and supports auditing.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Secrets Client](../secrets-client/README.md)
