# Filesystem Client Shared Skill

**File:** `skills/shared/filesystem-client/README.md`

**Version:** 1.0.0

---

# Purpose

The Filesystem Client Shared Skill provides the canonical,
implementation-independent mechanism for accessing files within the Robust
PenTest Platform (RPP).

Rather than allowing individual skills to read and write paths directly, this
shared skill centralizes path confinement, sandboxing, read and write
operations, metadata inspection, and observability behind a stable interface.

All packages that require filesystem access SHALL delegate to this shared skill.

---

# Goals

The Filesystem Client Shared Skill SHALL

- Abstract filesystem backends behind a stable interface
- Confine access to explicitly configured roots
- Prevent path traversal and symlink escape
- Read, write, list, and stat entries with bounded sizes
- Authenticate to remote filesystems through the
  [Authentication](../authentication/README.md) package where applicable
- Produce filesystem evidence
- Integrate with platform observability

---

# Non-Goals

The Filesystem Client Shared Skill SHALL NOT

- Detect vulnerabilities such as insecure permissions
- Produce security findings
- Interpret file contents as findings
- Execute files
- Modify files outside configured roots

The Filesystem Client provides confined, authorized file access and reports
metadata and contents as data. Interpretation belongs to domain skills.

---

# Design Principles

The Filesystem Client Shared Skill SHALL be

- Deterministic in bounds given the same configuration and inputs
- Confinement-first to prevent traversal at the boundary
- Bounded in file size and listing depth
- Governed
- Observable
- Secure by default

---

# Architecture

```
Master Agent

↓

Domain Skill

↓

Filesystem Client Shared Skill

├── Root Resolver
├── Path Confiner
├── Symlink Guard
├── Reader / Writer
├── Metadata Inspector
├── Evidence Manager
├── Event Manager

↓

Filesystem Adapter (local, remote, container)
```

The Filesystem Client performs operations but SHALL remain unaware of the
filesystem adapter implementation.

---

# Responsibilities

The Filesystem Client Shared Skill is responsible for

- Resolving operations against configured roots
- Confining every path within a root and rejecting traversal
- Preventing symlink escape beyond a root
- Reading, writing, listing, and stating entries with bounds
- Authenticating to remote filesystems where applicable
- Applying rate and retry governance
- Emitting filesystem lifecycle events and capturing evidence

---

# Operation Lifecycle

```
Receive Operation Request

↓

Acquire Rate Permit

↓

Resolve Root

↓

Confine And Canonicalize Path

↓

Guard Against Symlink Escape

↓

Perform Operation (bounded, authorized)

↓

Emit Evidence and Events
```

The operation outcome SHOULD be preserved as evidence.

---

# Path Confinement

The Filesystem Client SHALL resolve every path relative to a configured root and
SHALL canonicalize it.

A canonical path that escapes its root SHALL be rejected as a traversal
violation.

Absolute paths and parent references that would escape the root SHALL be
rejected.

This confinement is a safety boundary against path traversal regardless of caller
input.

---

# Symlink Handling

The Filesystem Client SHALL resolve symbolic links and SHALL reject any link that
resolves outside its root.

Where a policy disables link following, symbolic links SHALL be treated as
opaque entries.

---

# Operations

The Filesystem Client SHALL support

- read
- write
- append
- list
- stat
- delete

`write`, `append`, and `delete` SHALL be treated as intrusive and SHALL be gated
by authorization.

File sizes and listing depth SHALL be bounded; large contents SHALL be stored by
reference.

---

# Remote And Container Filesystems

Where a root maps to a remote or container filesystem, the Filesystem Client
SHALL authenticate through the [Authentication](../authentication/README.md)
package.

The same confinement and symlink guarantees SHALL apply regardless of backend.

---

# Governance

The Filesystem Client SHALL

- Acquire a permit from the [Rate Limiter](../rate-limiter/README.md) per
  operation
- Recover transient backend failures through the [Retry](../retry/README.md)
  shared skill

Write and delete operations SHALL be gated as intrusive.

---

# Evidence

The Filesystem Client Shared Skill SHOULD capture

- Root and confined path
- Operation kind
- Size and entry counts
- Metadata such as permissions and timestamps
- Operation outcome

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain sensitive
file contents unless explicitly authorized and redacted.

---

# Events

The Filesystem Client Shared Skill SHOULD publish

- OperationRequested
- PathConfined
- SymlinkResolved
- OperationCompleted
- TraversalRejected
- OperationFailed

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The Filesystem Client Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Authentication](../authentication/README.md)
- [Rate Limiter](../rate-limiter/README.md)
- [Retry](../retry/README.md)
- [Evidence Schema](../../../schemas/evidence.md)

The Filesystem Client Shared Skill SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Evidence and artifact staging within shared packages
- Configuration-review skills inspecting authorized paths
- Container and host review skills

---

# Outputs

Typical outputs MAY include

- File contents by reference
- Directory listings
- Entry metadata
- Filesystem evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Filesystem Client Shared Skill SHALL

- Confine all access within configured roots
- Reject path traversal and symlink escape
- Treat write and delete as intrusive
- Bound file size and listing depth
- Report metadata and contents as data, not findings
- Preserve auditability

Uncontrolled filesystem access can expose or destroy data. The shared skill SHALL
enforce confinement and authorization.

---

# Best Practices

Consumers SHOULD

- Operate within the narrowest sufficient root
- Prefer read and stat operations
- Bound file sizes and listing depth
- Authorize writes explicitly
- Capture operation evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Access paths directly outside the client
- Assume caller paths are safe
- Follow symlinks outside a root
- Perform unauthorized writes or deletes
- Persist sensitive file contents in evidence

---

# Documentation Requirements

This shared skill includes

- README.md
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md
- adr/ADR-001-filesystem-confinement-abstraction.md

---

# Related Shared Packages

- [Evidence](../evidence/README.md)
- [Authentication](../authentication/README.md)
- [Cache](../cache/README.md)

---

# Canonical Schemas

- [Evidence](../../../schemas/evidence.md)

---

# Architecture Decisions

- [ADR-001 — Filesystem Confinement Abstraction](adr/ADR-001-filesystem-confinement-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Content-addressed deduplicated storage
- Streaming read and write descriptors
- Change-watch subscriptions
- Extended attribute inspection

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Filesystem Client Shared Skill provides a confined, bounded, and
implementation-independent filesystem abstraction for the Robust PenTest
Platform.

It enables consistent, auditable file access across local, remote, and container
backends while preventing traversal and protecting data, without embedding
security interpretation or backend implementations in consumers.
