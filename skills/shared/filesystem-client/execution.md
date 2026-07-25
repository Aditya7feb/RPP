# Filesystem Client Execution Model

**File:** `skills/shared/filesystem-client/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the Filesystem Client Shared Skill.

The execution model describes how the shared skill performs an operation from
root resolution through path confinement, symlink guarding, and the operation
itself.

The model is deterministic in bounds given the same configuration and inputs.

---

# Execution Overview

```
Receive Operation Request

↓

Resolve Configuration

↓

Acquire Rate Permit

↓

Resolve Root

↓

Confine And Canonicalize Path

↓

Guard Against Symlink Escape

↓

Authorize Intrusive Operations

↓

Perform Operation (bounded)

↓

Emit Evidence and Events

↓

Return Result
```

---

# Stage 1 — Configuration Resolution

The Filesystem Client SHALL resolve roots, confinement, execution gating, and
bounds using the precedence defined in [configuration.md](configuration.md).

Confinement SHALL always be enforced.

---

# Stage 2 — Rate Permit

The Filesystem Client SHALL acquire a permit from the
[Rate Limiter](../rate-limiter/README.md) for the operation.

---

# Stage 3 — Root Resolution

The Filesystem Client SHALL resolve the referenced root and its backend.

For remote or container backends, authentication SHALL be resolved through the
[Authentication](../authentication/README.md) package.

---

# Stage 4 — Path Confinement

The Filesystem Client SHALL resolve the requested path relative to the root and
canonicalize it.

A canonical path escaping the root SHALL be rejected with `traversal_rejected`.

Absolute paths and parent references escaping the root SHALL be rejected.

---

# Stage 5 — Symlink Guard

The Filesystem Client SHALL resolve symbolic links.

A link resolving outside the root SHALL be rejected.

Where `follow_symlinks` is `false`, links SHALL be treated as opaque entries.

---

# Stage 6 — Authorization

`write`, `append`, and `delete` operations SHALL proceed only when the operation
is authorized and the root is `writable`.

Unauthorized intrusive operations SHALL be rejected.

---

# Stage 7 — Operation

The Filesystem Client SHALL perform the operation bounded by configured limits.

- `read` SHALL bound bytes by `max_read_bytes` and store large content by
  reference
- `write` and `append` SHALL bound bytes by `max_write_bytes`
- `list` SHALL bound entries and depth
- `stat` SHALL return metadata
- `delete` SHALL remove the confined entry

The Filesystem Client SHALL NOT execute files.

---

# Stage 8 — Evidence And Events

The Filesystem Client SHOULD emit operation evidence and lifecycle events
according to configuration. Evidence SHALL exclude sensitive contents.

---

# Retry Behavior

Transient backend failures MAY be retried through the
[Retry](../retry/README.md) shared skill, each retry acquiring a fresh permit.

Write and delete operations SHALL be retried only when idempotent and authorized.

---

# Determinism

Given identical configuration and inputs, the Filesystem Client SHALL enforce
identical confinement and bounds and produce identical outcome classifications
for the same observed backend state.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A rejected traversal SHALL never perform the operation.

A failed write SHALL NOT leave a partially written file where the backend
supports atomic replacement.

---

# Execution Outputs

The execution model SHALL produce

- Read content by reference
- Directory listings
- Entry metadata
- Operation metrics
- Evidence references

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Authentication](../authentication/README.md)
- [Execution Model](../../core/execution-model.md)
