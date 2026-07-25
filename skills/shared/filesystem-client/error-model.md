# Filesystem Client Error Model

**File:** `skills/shared/filesystem-client/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the Filesystem Client Shared Skill.

The error model classifies the failure conditions the shared skill MAY produce
and aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The Filesystem Client Shared Skill SHALL

- Produce canonical, structured errors
- Enforce confinement as a hard boundary
- Distinguish traversal rejections from ordinary not-found conditions
- Never leak sensitive contents

---

# Error Categories

The Filesystem Client maps its failures onto the canonical categories.

```
Configuration

Validation

Confinement

NotFound

Authorization

Authentication

Timeout

Governance

Adapter

Internal
```

---

# Configuration Errors

Raised when configuration is invalid.

Conditions

- A referenced root does not exist
- Confinement disabled
- A referenced default policy does not resolve

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when an invocation is malformed.

Conditions

- Missing root reference or path
- Inline secret supplied
- Invalid operation kind

Validation errors SHALL be non-retryable.

---

# Confinement Errors

Raised when a path escapes its root.

Conditions

- Traversal beyond the root
- Symlink resolving outside the root

Confinement errors SHALL be non-retryable and SHALL preserve the attempted path
for audit without performing the operation.

---

# Not-Found Errors

Raised when a confined path does not exist.

Not-found errors SHALL be distinguished from confinement rejections and MAY be
expected during discovery.

---

# Authorization Errors

Raised when an intrusive operation is not authorized.

Conditions

- Write or delete attempted when disabled
- Write attempted on a non-writable root

Authorization errors SHALL be non-retryable without a policy change.

---

# Authentication Errors

Raised when remote-backend authentication fails.

Authentication errors SHALL NOT expose credentials and SHALL be non-retryable
without new credentials.

---

# Timeout Errors

Raised when an operation exceeds its bound.

Timeout errors SHALL carry the breached bound.

---

# Governance Errors

Raised when an operation would violate governance.

Conditions

- Rate ceiling exceeded

Governance errors SHALL be non-retryable without operator intervention.

---

# Adapter Errors

Raised when an underlying filesystem adapter fails unexpectedly.

Adapter errors SHALL be normalized so that consumers remain unaware of the
implementation.

---

# Internal Errors

Raised for unexpected conditions within the Filesystem Client.

Internal errors SHALL be treated as non-retryable and SHOULD be reported for
diagnosis.

---

# Error Structure

Every error SHALL conform to the canonical error structure.

```yaml
category:

code:

message:

retryable:

root_id:

path:
```

`category` SHALL be one of the canonical categories.

`retryable` SHALL indicate whether the operation MAY be attempted again.

Errors SHALL NOT contain sensitive file contents.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| traversal_rejected | Confinement | No |
| symlink_escape | Confinement | No |
| not_found | NotFound | Context dependent |
| write_blocked | Authorization | No |
| auth_failed | Authentication | No |
| timed_out | Timeout | No |
| rejected | Governance | No |
| invalid_request | Validation | No |
| missing_root | Configuration | No |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# Confinement Principle

The Filesystem Client SHALL never perform an operation on a path that escapes its
root.

A traversal or symlink-escape attempt SHALL be rejected and preserved for audit
rather than silently normalized.

---

# Evidence

Errors SHOULD be captured as evidence conforming to the
[Evidence schema](../../../schemas/evidence.md), including the category, root, and
attempted path, and SHALL exclude sensitive contents.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [Authentication](../authentication/README.md)
