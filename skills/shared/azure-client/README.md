# Azure Client Shared Skill

**File:** `skills/shared/azure-client/README.md`

**Version:** 1.0.0

---

# Purpose

The Azure Client Shared Skill provides the canonical, implementation-independent
mechanism for interacting with Microsoft Azure control-plane and metadata services
within the Robust PenTest Platform (RPP).

Rather than allowing individual skills to call Azure Resource Manager and service APIs
directly, this shared skill centralizes service access, subscription and resource-group
scoping, resource description, mutation gating, instance-metadata observation, and
observability behind a stable interface exposing provider-native Azure resource models.

All packages that require Azure access SHALL delegate to this shared skill.

---

# Goals

The Azure Client Shared Skill SHALL

- Abstract Azure service access behind a stable, provider-native interface
- Perform service requests through the [HTTP Client](../http-client/README.md) over
  TLS
- Authenticate through the [Authentication](../authentication/README.md) package
- Confine operations to authorized subscriptions, resource groups, regions, and services
- Prefer read operations (get, list) and gate mutations as intrusive
- Observe Entra ID role assignments, compute, network, and configuration metadata and
  report it as data
- Observe the Azure Instance Metadata Service (IMDS) reachability and responses as data
- Produce Azure evidence
- Integrate with platform observability

---

# Non-Goals

The Azure Client Shared Skill SHALL NOT

- Detect vulnerabilities such as over-permissive role assignments or public exposure
- Produce security findings
- Classify risk
- Interpret role, network, or configuration metadata as security posture
- Contain cloud-domain assessment logic
- Perform mutations without authorization
- Perform unbounded enumeration

The Azure Client performs confined, authorized service access and reports provider-native
metadata as data. Interpretation, including misconfiguration and exposure assessment,
belongs to the Azure Cloud Security domain skill.

---

# Design Principles

The Azure Client Shared Skill SHALL be

- Deterministic in bounds given the same configuration and inputs
- Scope-confined to authorized subscriptions, resource groups, regions, and services
- Provider-native — it exposes Azure resource models without abstracting them away
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

Azure Client Shared Skill

├── Service Connector       → HTTP Client (TLS)
├── Scope Confiner          (subscription · resource-group · region · service)
├── Resource Describer      (get · list)
├── Mutation Gatekeeper     → Policy Engine
├── Role Inspector          (Entra ID / RBAC)
├── Metadata Observer       (IMDS)
├── Pagination Bounder
├── Evidence Manager
├── Event Manager

↓

Azure Resource Manager And Service APIs
```

The Azure Client performs operations but SHALL remain unaware of the API transport
implementation, which is provided by the HTTP and TLS shared skills.

---

# Responsibilities

The Azure Client Shared Skill is responsible for

- Connecting to Azure service endpoints via the [HTTP Client](../http-client/README.md)
- Authenticating via the [Authentication](../authentication/README.md) package and
  resolving credentials through the [Secrets Client](../secrets-client/README.md)
- Confining operations to authorized subscriptions, resource groups, regions, and services
- Performing get and list operations and, where authorized, mutating operations
- Observing Entra ID role assignments, compute, network, and configuration metadata and
  reporting it as data
- Observing instance metadata service responses as data
- Applying rate and retry governance
- Emitting Azure lifecycle events and capturing evidence

---

# Operation Lifecycle

```
Receive Operation Request

↓

Acquire Rate Permit

↓

Confine To Authorized Scope (subscription · resource-group · region · service)

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

The Azure Client SHALL confine operations to configured subscriptions, resource groups,
regions, and services.

A resource outside an authorized scope SHALL be rejected regardless of caller input.

Cross-subscription operations SHALL require explicit cross-subscription authorization.

---

# Read And Mutation Operations

The Azure Client SHALL support

- get
- list
- create
- update
- delete
- tag

`get` and `list` SHALL be read operations preferred by default.

`create`, `update`, `delete`, and `tag` SHALL be treated as intrusive and SHALL be
gated by the [Policy Engine](../policy-engine/README.md). Result sets and pagination
depth SHALL be bounded.

---

# Role Observation

The Azure Client SHALL observe Entra ID role assignments and effective permissions and
SHALL report them as data.

Whether observed role assignments represent an over-permissive condition SHALL be
interpreted by the domain skill, not this client.

---

# Instance Metadata Observation

The Azure Client SHALL observe the reachability and responses of the Azure Instance
Metadata Service (IMDS) and SHALL report them as data. Whether metadata reachability
represents a weakness SHALL be interpreted by the domain skill.

---

# Authentication

The Azure Client SHALL authenticate through the
[Authentication](../authentication/README.md) package, supporting

- service_principal
- managed_identity
- access_token

Secrets and tokens SHALL be resolved through the
[Secrets Client](../secrets-client/README.md) and SHALL NOT appear in evidence or logs.

---

# Governance

The Azure Client SHALL

- Acquire a permit from the [Rate Limiter](../rate-limiter/README.md) per operation
- Route through the [Proxy](../proxy/README.md) shared skill where configured
- Recover transient failures through the [Retry](../retry/README.md) shared skill

Mutations SHALL be gated as intrusive through the
[Policy Engine](../policy-engine/README.md).

---

# Evidence

The Azure Client Shared Skill SHOULD capture

- Subscription, resource-group, region, and service identifiers
- Resource type and operation
- Result counts and pagination bounds
- Observed role, network, and configuration metadata
- Operation outcome

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain secrets,
credentials, or sensitive resource contents unless explicitly authorized and redacted.

---

# Events

The Azure Client Shared Skill SHOULD publish

- ServiceConnected
- ScopeConfined
- ResourceDescribed
- ResourceMutated
- RoleObserved
- MetadataObserved
- OperationFailed

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The Azure Client Shared Skill depends on

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

The Azure Client Shared Skill SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- The Azure Cloud Security assessment skill
- Cloud asset-discovery skills enumerating Azure resources

---

# Outputs

Typical outputs MAY include

- Provider-native resource descriptions by reference
- Role observation records
- Instance metadata observation records
- Azure evidence references

Outputs SHALL remain implementation independent while preserving Azure resource models.

---

# Security Principles

The Azure Client Shared Skill SHALL

- Confine access to authorized subscriptions, resource groups, regions, and services
- Prefer read operations and gate mutations as intrusive
- Protect credentials from evidence and logs
- Report role, network, and configuration metadata as data, not findings
- Preserve auditability

Azure mutations can cause irreversible changes. The shared skill SHALL enforce
confinement and gate mutations through the Policy Engine.

---

# Best Practices

Consumers SHOULD

- Operate within the narrowest authorized subscription and resource-group scope
- Prefer get and list
- Bound result sets and pagination depth
- Capture operation evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Call Azure service APIs directly
- Access resources outside authorized scopes
- Perform unauthorized mutations
- Interpret roles or configuration as findings within the transport layer
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
- adr/ADR-001-azure-service-abstraction.md

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

- [ADR-001 — Azure Service Abstraction](adr/ADR-001-azure-service-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Management-group and tenant awareness
- Azure Policy state snapshots
- Cross-region aggregation descriptors
- Additional service coverage

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Azure Client Shared Skill provides a confined, bounded, and
implementation-independent Azure service abstraction that preserves provider-native
resource models for the Robust PenTest Platform.

It enables consistent, auditable Azure interaction atop the HTTP and TLS shared skills
while enforcing scope and gating mutations, without embedding security interpretation or
API implementations in consumers.
