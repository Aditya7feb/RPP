# Cloud Storage Client Shared Skill

**File:** `skills/shared/cloud-storage-client/README.md`

**Version:** 1.0.0

---

# Purpose

The Cloud Storage Client Shared Skill provides the canonical,
implementation-independent mechanism for accessing object storage within the
Robust PenTest Platform (RPP).

Rather than allowing individual skills to call provider storage services
directly, this shared skill centralizes bucket and object operations, encryption
enforcement, access-metadata observation, presigned-reference handling, and
observability behind a stable interface.

All packages that require object-storage access SHALL delegate to this shared
skill.

---

# Goals

The Cloud Storage Client Shared Skill SHALL

- Abstract object-storage providers behind a stable interface
- List, read, write, stat, and delete objects within authorized scopes
- Enforce server-side encryption where mandated
- Observe and report access metadata such as public exposure as data
- Authenticate through the [Authentication](../authentication/README.md) package
- Produce storage evidence
- Integrate with platform observability

---

# Non-Goals

The Cloud Storage Client Shared Skill SHALL NOT

- Detect vulnerabilities such as public-bucket misconfiguration
- Produce security findings
- Interpret access metadata as findings
- Modify access policy without authorization
- Perform unbounded downloads

The Cloud Storage Client provides confined, authorized object access and reports
metadata as data. Interpretation, including public-exposure assessment, belongs to
cloud domain skills.

---

# Design Principles

The Cloud Storage Client Shared Skill SHALL be

- Deterministic in bounds given the same configuration and inputs
- Scope-confined to authorized buckets and prefixes
- Encryption-aware
- Bounded in object size and listing volume
- Governed
- Secure by default

---

# Architecture

```
Master Agent

↓

Cloud Domain Skill

↓

Cloud Storage Client Shared Skill

├── Scope Confiner
├── Object Reader / Writer
├── Encryption Enforcer
├── Access-Metadata Inspector
├── Presigned Reference Handler
├── Evidence Manager
├── Event Manager

↓

Provider Adapter
```

The Cloud Storage Client performs operations but SHALL remain unaware of the
provider adapter implementation.

---

# Responsibilities

The Cloud Storage Client Shared Skill is responsible for

- Confining operations to authorized buckets and prefixes
- Listing, reading, writing, stating, and deleting objects with bounds
- Enforcing server-side encryption where mandated
- Observing access metadata and reporting it as data
- Handling presigned references without exposing long-lived secrets
- Applying rate and retry governance
- Emitting storage lifecycle events and capturing evidence

---

# Operation Lifecycle

```
Receive Operation Request

↓

Acquire Rate Permit

↓

Confine To Authorized Scope

↓

Authenticate

↓

Enforce Encryption (for writes)

↓

Perform Operation (bounded, authorized)

↓

Observe Access Metadata

↓

Emit Evidence and Events
```

The operation outcome SHOULD be preserved as evidence.

---

# Scope Confinement

The Cloud Storage Client SHALL confine operations to configured buckets and
prefixes.

An object key outside an authorized scope SHALL be rejected.

This confinement prevents access to unauthorized buckets regardless of caller
input.

---

# Encryption

For writes, the Cloud Storage Client SHALL enforce server-side encryption where
mandated by configuration.

Where encryption is required and unavailable, the write SHALL fail rather than
store unencrypted data.

Client-side encryption keys, where used, SHALL be resolved through the
[Secrets Client](../secrets-client/README.md) and never exposed.

---

# Access-Metadata Observation

The Cloud Storage Client SHALL observe access metadata such as ACLs, public-access
flags, and encryption status, and SHALL report them as data.

Whether metadata represents a misconfiguration SHALL be interpreted by cloud
domain skills, not this client.

---

# Presigned References

The Cloud Storage Client SHALL support generating and consuming presigned
references with bounded lifetimes.

Presigned references SHALL be treated as sensitive, redacted from evidence, and
bounded to the minimum necessary lifetime.

---

# Governance

The Cloud Storage Client SHALL

- Acquire a permit from the [Rate Limiter](../rate-limiter/README.md) per
  operation
- Recover transient provider failures through the [Retry](../retry/README.md)
  shared skill

Write, delete, and policy-affecting operations SHALL be gated as intrusive.

---

# Evidence

The Cloud Storage Client Shared Skill SHOULD capture

- Bucket, prefix, and object key
- Operation kind
- Object size and count
- Access metadata such as public flag and encryption status
- Operation outcome

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain object
contents or presigned references unless explicitly authorized and redacted.

---

# Events

The Cloud Storage Client Shared Skill SHOULD publish

- OperationRequested
- ScopeConfined
- ObjectRead
- ObjectWritten
- AccessMetadataObserved
- OperationFailed

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The Cloud Storage Client Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Authentication](../authentication/README.md)
- [Secrets Client](../secrets-client/README.md)
- [Rate Limiter](../rate-limiter/README.md)
- [Retry](../retry/README.md)
- [Evidence Schema](../../../schemas/evidence.md)

The Cloud Storage Client Shared Skill SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Cloud asset-discovery skills
- Bucket-exposure assessment skills
- Evidence and artifact staging to authorized storage

---

# Outputs

Typical outputs MAY include

- Object listings
- Object contents by reference
- Access metadata
- Storage evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Cloud Storage Client Shared Skill SHALL

- Confine access to authorized buckets and prefixes
- Enforce encryption where mandated
- Treat write, delete, and policy changes as intrusive
- Protect presigned references and keys from evidence and logs
- Report access metadata as data, not findings
- Preserve auditability

Object storage often contains sensitive data. The shared skill SHALL enforce
confinement, encryption, and authorization.

---

# Best Practices

Consumers SHOULD

- Operate within the narrowest authorized scope
- Prefer read and stat operations
- Require encryption for writes
- Bound object sizes and listing volume
- Capture operation evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Call provider storage services directly
- Access buckets outside authorized scopes
- Store unencrypted data where encryption is required
- Modify access policy without authorization
- Persist object contents or presigned references in evidence

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
- adr/ADR-001-cloud-storage-abstraction.md

---

# Related Shared Packages

- [Authentication](../authentication/README.md)
- [Secrets Client](../secrets-client/README.md)
- [Filesystem Client](../filesystem-client/README.md)
- [Evidence](../evidence/README.md)

---

# Canonical Schemas

- [Evidence](../../../schemas/evidence.md)

---

# Architecture Decisions

- [ADR-001 — Cloud Storage Abstraction](adr/ADR-001-cloud-storage-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Multipart and resumable transfers
- Versioned-object inspection
- Lifecycle-policy observation
- Cross-provider replication descriptors

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Cloud Storage Client Shared Skill provides a confined, bounded, and
implementation-independent object-storage abstraction for the Robust PenTest
Platform.

It enables consistent, auditable object access across providers while enforcing
scope and encryption and protecting sensitive references, without embedding
security interpretation or provider implementations in consumers.
