# Kubernetes Client Shared Skill

**File:** `skills/shared/kubernetes-client/README.md`

**Version:** 1.0.0

---

# Purpose

The Kubernetes Client Shared Skill provides the canonical,
implementation-independent mechanism for interacting with Kubernetes API servers
within the Robust PenTest Platform (RPP).

Rather than allowing individual skills to call the Kubernetes API directly, this
shared skill centralizes API access, namespace scoping, resource operations,
mutation gating, RBAC observation, and observability behind a stable interface.

All packages that require Kubernetes access SHALL delegate to this shared skill.

---

# Goals

The Kubernetes Client Shared Skill SHALL

- Abstract the Kubernetes API behind a stable interface
- Perform API requests through the [HTTP Client](../http-client/README.md) over
  TLS
- Authenticate through the [Authentication](../authentication/README.md) package
- Confine operations to authorized namespaces and resource scopes
- Prefer read operations and gate mutations as intrusive
- Observe RBAC and resource metadata and report it as data
- Produce Kubernetes evidence
- Integrate with platform observability

---

# Non-Goals

The Kubernetes Client Shared Skill SHALL NOT

- Detect vulnerabilities such as over-permissive RBAC
- Produce security findings
- Interpret resource or RBAC metadata as findings
- Perform cluster mutations without authorization
- Execute workloads implicitly

The Kubernetes Client performs confined, authorized API operations and reports
metadata as data. Interpretation, including RBAC and misconfiguration assessment,
belongs to cloud and container domain skills.

---

# Design Principles

The Kubernetes Client Shared Skill SHALL be

- Deterministic in bounds given the same configuration and inputs
- Namespace and scope confined
- Read-preferring with explicit mutation gating
- Bounded in result size and watch duration
- Governed
- Secure by default

---

# Architecture

```
Master Agent

↓

Cloud or Container Domain Skill

↓

Kubernetes Client Shared Skill

├── Cluster Connector       → HTTP Client (TLS)
├── Scope Confiner
├── Resource Operator
├── Mutation Gatekeeper
├── RBAC Inspector
├── Watch Manager
├── Evidence Manager
├── Event Manager

↓

Kubernetes API Server
```

The Kubernetes Client performs operations but SHALL remain unaware of the API
transport implementation, which is provided by the HTTP and TLS shared skills.

---

# Responsibilities

The Kubernetes Client Shared Skill is responsible for

- Connecting to an API server via the [HTTP Client](../http-client/README.md)
- Authenticating via the [Authentication](../authentication/README.md) package
  and resolving tokens through the [Secrets Client](../secrets-client/README.md)
- Confining operations to authorized namespaces and resource kinds
- Performing get, list, watch, and, where authorized, mutating operations
- Observing RBAC and resource metadata and reporting it as data
- Applying rate and retry governance
- Emitting Kubernetes lifecycle events and capturing evidence

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

Gate Mutations (if any)

↓

Perform Operation (bounded, authorized)

↓

Observe RBAC / Metadata

↓

Emit Evidence and Events
```

The operation outcome SHOULD be preserved as evidence.

---

# Scope Confinement

The Kubernetes Client SHALL confine operations to configured namespaces and
resource kinds.

A resource outside an authorized scope SHALL be rejected.

Cluster-scoped operations SHALL require explicit cluster-scope authorization.

This confinement prevents access to unauthorized resources regardless of caller
input.

---

# Read And Mutation Operations

The Kubernetes Client SHALL support

- get
- list
- watch
- create
- update
- patch
- delete
- exec

`get`, `list`, and `watch` SHALL be read operations preferred by default.

`create`, `update`, `patch`, `delete`, and `exec` SHALL be treated as intrusive
and SHALL be gated by authorization. `exec` and `attach` operations SHALL require
elevated, explicit authorization because they execute in workloads.

Result sets and watch durations SHALL be bounded.

---

# RBAC Observation

The Kubernetes Client SHALL observe effective permissions, such as through
access-review requests, and SHALL report them as data.

Whether observed RBAC represents an over-permissive condition SHALL be
interpreted by domain skills, not this client.

---

# Authentication

The Kubernetes Client SHALL authenticate through the
[Authentication](../authentication/README.md) package, supporting

- bearer_token
- client_certificate
- exec_credential

Tokens and keys SHALL be resolved through the
[Secrets Client](../secrets-client/README.md) and SHALL NOT appear in evidence or
logs.

---

# Governance

The Kubernetes Client SHALL

- Acquire a permit from the [Rate Limiter](../rate-limiter/README.md) per
  operation
- Route through the [Proxy](../proxy/README.md) shared skill where configured,
  such as through an API-server bastion
- Recover transient failures through the [Retry](../retry/README.md) shared skill

Mutations and `exec` operations SHALL be gated as intrusive.

---

# Evidence

The Kubernetes Client Shared Skill SHOULD capture

- Cluster and namespace identifiers
- Resource kind and operation
- Result counts
- Observed RBAC and resource metadata
- Operation outcome

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain secrets,
tokens, or sensitive resource contents unless explicitly authorized and redacted.

---

# Events

The Kubernetes Client Shared Skill SHOULD publish

- ClusterConnected
- ScopeConfined
- ResourceRead
- ResourceMutated
- RbacObserved
- WatchClosed
- OperationFailed

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The Kubernetes Client Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [HTTP Client](../http-client/README.md)
- [Authentication](../authentication/README.md)
- [Secrets Client](../secrets-client/README.md)
- [Rate Limiter](../rate-limiter/README.md)
- [Retry](../retry/README.md)
- [Evidence Schema](../../../schemas/evidence.md)

The Kubernetes Client Shared Skill SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Kubernetes assessment skills
- Container-platform review skills
- Cloud asset-discovery skills enumerating clusters

---

# Outputs

Typical outputs MAY include

- Resource listings and objects by reference
- RBAC observation records
- Watch event streams within bounds
- Kubernetes evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Kubernetes Client Shared Skill SHALL

- Confine access to authorized namespaces and resource kinds
- Prefer read operations and gate mutations as intrusive
- Require elevated authorization for workload execution
- Protect tokens and keys from evidence and logs
- Report RBAC and metadata as data, not findings
- Preserve auditability

Cluster mutations and workload execution can cause irreversible changes. The
shared skill SHALL enforce confinement and authorization.

---

# Best Practices

Consumers SHOULD

- Operate within the narrowest authorized namespace scope
- Prefer get, list, and watch
- Require elevated authorization for exec
- Bound result sets and watch durations
- Capture operation evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Call the Kubernetes API directly
- Access resources outside authorized scopes
- Perform unauthorized mutations or exec
- Interpret RBAC as findings within the transport layer
- Persist tokens or sensitive resource contents in evidence

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
- adr/ADR-001-kubernetes-api-abstraction.md

---

# Related Shared Packages

- [HTTP Client](../http-client/README.md)
- [Authentication](../authentication/README.md)
- [Secrets Client](../secrets-client/README.md)
- [Cloud Storage Client](../cloud-storage-client/README.md)

---

# Canonical Schemas

- [Evidence](../../../schemas/evidence.md)
- [HTTP Transaction](../../../schemas/http-transaction.md)

---

# Architecture Decisions

- [ADR-001 — Kubernetes API Abstraction](adr/ADR-001-kubernetes-api-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Custom resource definition awareness
- Server-side apply descriptors
- Admission-review observation
- Multi-cluster context federation

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Kubernetes Client Shared Skill provides a confined, bounded, and
implementation-independent Kubernetes API abstraction for the Robust PenTest
Platform.

It enables consistent, auditable cluster interaction atop the HTTP and TLS shared
skills while enforcing scope and gating mutations, without embedding security
interpretation or API implementations in consumers.
