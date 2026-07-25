# Filesystem Client Examples

**File:** `skills/shared/filesystem-client/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
Filesystem Client Shared Skill in use.

Examples demonstrate confined reads, traversal rejection, symlink guarding, write
gating, listings, evidence, and expected outputs.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Confined Read

A configuration-review skill reads a file within an authorized root.

## Invocation

```yaml
metadata:
  request_id: req-9801
  assessment_id: asmt-42
  task_id: task-config-review
  skill_id: config-review
root_id: target-host
path: ssh/sshd_config
kind: read
options:
  max_bytes: 1MB
```

## Result

```yaml
outcome: completed
content_ref: artifact://fs/req-9801-sshd_config
metadata:
  size: 3218
  permissions: "0644"
```

The read is confined within the `target-host` root and stored by reference.

---

# Example 2 — Traversal Rejected

A path attempts to escape its root.

## Invocation

```yaml
root_id: target-host
path: ../../etc/shadow
kind: read
```

## Result

```yaml
outcome: traversal_rejected
error:
  category: Confinement
  code: traversal_rejected
  root_id: target-host
  path: ../../etc/shadow
  retryable: false
```

The confinement boundary prevents access outside the root.

---

# Example 3 — Symlink Escape Rejected

A symlink resolves outside the root.

## Configuration

```yaml
confinement:
  follow_symlinks: true
```

## Result

```yaml
outcome: traversal_rejected
error:
  category: Confinement
  code: symlink_escape
  retryable: false
```

Links resolving outside the root are rejected even when following is enabled.

---

# Example 4 — Write Blocked

A write is attempted while writes are disabled.

## Configuration

```yaml
execution:
  allow_write: false
```

## Result

```yaml
outcome: rejected
error:
  category: Authorization
  code: write_blocked
  retryable: false
```

Writes are intrusive and require authorization and a writable root.

---

# Example 5 — Directory Listing

A skill lists a directory with bounded depth.

## Invocation

```yaml
root_id: target-host
path: cron.d
kind: list
options:
  max_depth: 1
  max_entries: 1000
```

## Result

```yaml
outcome: completed
entries:
  - name: app-backup
    type: file
    size: 214
  - name: logrotate
    type: file
    size: 180
```

Listings are bounded by depth and entry count.

---

# Example 6 — Authorized Staging Write

An evidence-staging write occurs within a writable staging root.

## Configuration

```yaml
roots:
  - root_id: staging
    writable: true
execution:
  allow_write: true
```

## Result

```yaml
outcome: completed
metadata:
  size: 4096
```

The write succeeds within the confined, writable staging root.

---

# Example 7 — Evidence Record

A single operation produces the following evidence.

```yaml
evidence:
  type: filesystem-operation
  root_id: target-host
  path: ssh/sshd_config
  kind: read
  size: 3218
  permissions: "0644"
  decided_at: 2026-07-25T17:00:00Z
```

The evidence conforms to the canonical
[Evidence schema](../../../schemas/evidence.md), excludes sensitive contents, and
supports auditing.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Evidence](../evidence/README.md)
