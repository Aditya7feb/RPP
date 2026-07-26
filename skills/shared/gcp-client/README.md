# GCP Client Shared Skill

**File:** `skills/shared/gcp-client/README.md`

**Version:** 1.0.0

---

# Purpose

The GCP Client Shared Skill provides the canonical, implementation-independent mechanism
for interacting with Google Cloud Platform control-plane and metadata services within the
Robust PenTest Platform (RPP).

Rather than allowing individual skills to call GCP service APIs directly, this shared skill
centralizes service access, project and region scoping, resource description, mutation
gating, metadata-server observation, and observability behind a stable interface exposing
provider-native GCP resource models.

All packages that require GCP access SHALL delegate to this shared skill.

---

# Goals

The GCP Client Shared Skill SHALL

- Abstract GCP service access behind a stable, provider-native interface
- Perform service requests through the [HTTP Client](../http-client/README.md) over TLS
- Authenticate through the [Authentication](../authentication/README.md) package
- Confine operations to authorized organizations, projects, regions, and services
- Prefer read operations (get, list) and gate mutations as intrusive
- Observe IAM policy bindings, compute, network, and configuration metadata and report it
  as data
- Observe the GCP metadata server reachability and responses as data
- Produce GCP evidence
- Integrate with platform observability

---

# Non-Goals

The GCP Client Shared Skill SHALL NOT

- Detect vulnerabilities such as over-permissive IAM bindings or public exposure
- Produce security findings
- Classify risk
- Interpret IAM, network, or configuration metadata as security posture
- Contain cloud-domain assessment logic
- Perform mutations without authorization
- Perform unbounded enumeration

The GCP Client performs confined, authorized service access and reports provider-native
metadata as data. Interpretation, including misconfiguration and exposure assessment,
belongs to the GCP Cloud Security domain skill.

---

# Design Principles

The GCP Client Shared Skill SHALL be

- Deterministic in bounds given the same configuration and inputs
- Scope-confined to authorized organizations, projects, regions, and services
- Provider-native — it exposes GCP resource models without abstracting them away
- Read-preferring with explicit mutation gating
- Bounded in result size and pagination depth
- Governed
- Secure by default

---

# Architecture

```
Master Agent

↓

Cloud Security Domain Skill

↓

GCP Client Shared Skill

├── Service Connector       → HTTP Client (TLS)
├── Scope Confiner          (organization · project · region · service)
├── Resource Describer      (get · list)
├── Mutation Gatekeeper     → Policy Engine
├── IAM Inspector           (policy bindings)
├── Metadata Observer       (metadata server)
├── Pagination Bounder
├── Evidence Manager
├── Event Manager

↓

GCP Service APIs
```

The GCP Client performs operations but SHALL remain unaware of the API transport
implementation, which is provided by the HTTP and TLS shared skills.

---

# Responsibilities

The GCP Client Shared Skill is responsible for

- Connecting to GCP service endpoints via the [HTTP Client](../http-client/README.md)
- Authenticating via the [Authentication](../authentication/README.md) package and
  resolving credentials through the [Secrets Client](../secrets-client/README.md)
- Confining operations to authorized organizations, projects, regions, and services
- Performing get and list operations and, where authorized, mutating operations
- Observing IAM policy bindings, compute, network, and configuration metadata and
  reporting it as data
- Observing metadata server responses as data
- Applying rate and retry governance
- Emitting GCP lifecycle events and capturing evidence

---

# Operation Lifecycle

```
Receive Operation Request

↓

Acquire Rate Permit

↓

Confine To Authorized Scope (organization · project · region · service)

↓

Authenticate

↓

Gate Mutations (if any) → Policy Engine

↓

Perform Operation (bounded, authorized)

↓

Observe Provider-Native Metadata

↓

Emit Evidence and Events
```

The operation outcome SHOULD be preserved as evidence.

---

# Scope Confinement

The GCP Client SHALL confine operations to configured organizations, projects, regions,
and services.

A resource outside an authorized scope SHALL be rejected regardless of caller input.

Cross-project operations SHALL require explicit cross-project authorization.

---

# Read And Mutation Operations

The GCP Client SHALL support

- get
- list
- create
- update
- delete
- set-iam-policy

`get` and `list` SHALL be read operations preferred by default.

`create`, `update`, `delete`, and `set-iam-policy` SHALL be treated as intrusive and SHALL
be gated by the [Policy Engine](../policy-engine/README.md). Result sets and pagination
depth SHALL be bounded.

---

# IAM Observation

The GCP Client SHALL observe IAM policy bindings and effective permissions, such as through
get-iam-policy and testable-permission requests, and SHALL report them as data.

Whether observed IAM bindings represent an over-permissive condition SHALL be interpreted by
the domain skill, not this client.

---

# Metadata Observation

The GCP Client SHALL observe the reachability and responses of the GCP metadata server and
SHALL report them as data. Whether metadata reachability represents a weakness SHALL be
interpreted by the domain skill.

---

# Authentication

The GCP Client SHALL authenticate through the
[Authentication](../authentication/README.md) package, supporting

- service_account_key
- workload_identity
- access_token

Keys and tokens SHALL be resolved through the
[Secrets Client](../secrets-client/README.md) and SHALL NOT appear in evidence or logs.

---

# Governance

The GCP Client SHALL

- Acquire a permit from the [Rate Limiter](../rate-limiter/README.md) per operation
- Route through the [Proxy](../proxy/README.md) shared skill where configured
- Recover transient failures through the [Retry](../retry/README.md) shared skill

Mutations SHALL be gated as intrusive through the
[Policy Engine](../policy-engine/README.md).

---

# Evidence

The GCP Client Shared Skill SHOULD capture

- Organization, project, region, and service identifiers
- Resource type and operation
- Result counts and pagination bounds
- Observed IAM, network, and configuration metadata
- Operation outcome

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain secrets, credentials,
or sensitive resource contents unless explicitly authorized and redacted.

---

# Events

The GCP Client Shared Skill SHOULD publish

- ServiceConnected
- ScopeConfined
- ResourceDescribed
- ResourceMutated
- IamObserved
- MetadataObserved
- OperationFailed

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The GCP Client Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [HTTP Client](../http-client/README.md)
- [Authentication](../authentication/README.md)
- [Secrets Client](../secrets-client/README.md)
- [Policy Engine](../policy-engine/README.md)
- [Proxy](../proxy/README.md)
- [Rate Limiter](../rate-limiter/README.md)
- [Retry](../retry/README.md)
- [Evidence Schema](../../../schemas/evidence.md)

The GCP Client Shared Skill SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- The GCP Cloud Security assessment skill
- Cloud asset-discovery skills enumerating GCP resources

---

# Outputs

Typical outputs MAY include

- Provider-native resource descriptions by reference
- IAM observation records
- Metadata server observation records
- GCP evidence references

Outputs SHALL remain implementation independent while preserving GCP resource models.

---

# Security Principles

The GCP Client Shared Skill SHALL

- Confine access to authorized organizations, projects, regions, and services
- Prefer read operations and gate mutations as intrusive
- Protect credentials from evidence and logs
- Report IAM, network, and configuration metadata as data, not findings
- Preserve auditability

GCP mutations can cause irreversible changes. The shared skill SHALL enforce confinement
and gate mutations through the Policy Engine.

---

# Best Practices

Consumers SHOULD

- Operate within the narrowest authorized project and region scope
- Prefer get and list
- Bound result sets and pagination depth
- Capture operation evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Call GCP service APIs directly
- Access resources outside authorized scopes
- Perform unauthorized mutations
- Interpret IAM or configuration as findings within the transport layer
- Persist credentials or sensitive resource contents in evidence

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
- adr/ADR-001-gcp-service-abstraction.md

---

# Related Shared Packages

- [HTTP Client](../http-client/README.md)
- [Authentication](../authentication/README.md)
- [Secrets Client](../secrets-client/README.md)
- [Cloud Storage Client](../cloud-storage-client/README.md)
- [Policy Engine](../policy-engine/README.md)

---

# Canonical Schemas

- [Evidence](../../../schemas/evidence.md)
- [HTTP Transaction](../../../schemas/http-transaction.md)

---

# Architecture Decisions

- [ADR-001 — GCP Service Abstraction](adr/ADR-001-gcp-service-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Organization-policy and folder awareness
- Asset-inventory snapshots
- Cross-region aggregation descriptors
- Additional service coverage

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant GCP Client Shared Skill provides a confined, bounded, and
implementation-independent GCP service abstraction that preserves provider-native resource
models for the Robust PenTest Platform.

It enables consistent, auditable GCP interaction atop the HTTP and TLS shared skills while
enforcing scope and gating mutations, without embedding security interpretation or API
implementations in consumers.
