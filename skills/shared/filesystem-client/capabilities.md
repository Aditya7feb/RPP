# Filesystem Client Capabilities

**File:** `skills/shared/filesystem-client/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Filesystem Client Shared
Skill. Capabilities describe *what* the shared skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[Filesystem Client Interface](interface.md).

---

# Capability Model

```
Confinement

Read

Write

Metadata

Remote Access

Governance

Observability
```

---

# Confinement Capabilities

## Root Resolution

The Filesystem Client SHALL resolve operations against configured roots.

---

## Path Confinement

The Filesystem Client SHALL confine every path within its root and reject
traversal.

---

## Symlink Guard

The Filesystem Client SHALL reject symbolic links resolving outside a root.

---

# Read Capabilities

## Read

The Filesystem Client SHALL read files with bounded size.

---

## List

The Filesystem Client SHALL list directories with bounded depth.

---

# Write Capabilities

## Write And Append

The Filesystem Client SHALL write and append with authorization.

---

## Delete

The Filesystem Client SHALL delete entries with authorization.

---

## Intrusive Gating

The Filesystem Client SHALL gate write, append, and delete as intrusive.

---

# Metadata Capabilities

## Stat

The Filesystem Client SHALL return entry metadata such as size, permissions, and
timestamps.

---

# Remote Access Capabilities

## Backend Abstraction

The Filesystem Client SHALL access local, remote, and container backends behind a
uniform interface.

---

## Authentication

The Filesystem Client SHALL authenticate to remote backends through the
[Authentication](../authentication/README.md) package.

---

# Governance Capabilities

## Rate Governance

The Filesystem Client SHALL acquire a rate permit per operation through the
[Rate Limiter](../rate-limiter/README.md).

---

## Retry Governance

The Filesystem Client MAY retry transient backend failures through the
[Retry](../retry/README.md) shared skill.

---

# Observability Capabilities

## Evidence Capture

The Filesystem Client SHOULD capture operation evidence conforming to the
[Evidence schema](../../../schemas/evidence.md).

---

## Event Emission

The Filesystem Client SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The Filesystem Client SHOULD expose metrics including operations, bytes read,
bytes written, and entries listed.

---

# Capability Boundaries

The Filesystem Client SHALL NOT

- Detect insecure permissions or other vulnerabilities
- Produce findings
- Execute files
- Access paths outside configured roots
- Persist sensitive contents without authorization

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Root Resolution | Confinement | SHALL |
| Path Confinement | Confinement | SHALL |
| Symlink Guard | Confinement | SHALL |
| Read | Read | SHALL |
| List | Read | SHALL |
| Write And Append | Write | SHALL |
| Delete | Write | SHALL |
| Intrusive Gating | Write | SHALL |
| Stat | Metadata | SHALL |
| Backend Abstraction | Remote Access | SHALL |
| Authentication | Remote Access | SHALL |
| Rate Governance | Governance | SHALL |
| Retry Governance | Governance | MAY |
| Evidence Capture | Observability | SHOULD |
| Event Emission | Observability | SHOULD |
| Metrics | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Evidence Schema](../../../schemas/evidence.md)
