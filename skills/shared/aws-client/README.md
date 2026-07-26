# AWS Client Shared Skill

**File:** `skills/shared/aws-client/README.md`

**Version:** 1.0.0

---

# Purpose

The AWS Client Shared Skill provides the canonical, implementation-independent
mechanism for interacting with Amazon Web Services control-plane and metadata
services within the Robust PenTest Platform (RPP).

Rather than allowing individual skills to call AWS service APIs directly, this shared
skill centralizes service access, region and account scoping, resource description,
mutation gating, instance-metadata observation, and observability behind a stable
interface exposing provider-native AWS resource models.

All packages that require AWS access SHALL delegate to this shared skill.

---

# Goals

The AWS Client Shared Skill SHALL

- Abstract AWS service access behind a stable, provider-native interface
- Perform service requests through the [HTTP Client](../http-client/README.md) over
  TLS
- Authenticate through the [Authentication](../authentication/README.md) package
- Confine operations to authorized accounts, regions, and services
- Prefer read operations (describe, list, get) and gate mutations as intrusive
- Observe IAM, compute, network, and configuration metadata and report it as data
- Observe the instance metadata service (IMDS) reachability and responses as data
- Produce AWS evidence
- Integrate with platform observability

---

# Non-Goals

The AWS Client Shared Skill SHALL NOT

- Detect vulnerabilities such as over-permissive IAM policies or public exposure
- Produce security findings
- Classify risk
- Interpret IAM, network, or configuration metadata as security posture
- Contain cloud-domain assessment logic
- Perform mutations without authorization
- Perform unbounded enumeration

The AWS Client performs confined, authorized service access and reports provider-native
metadata as data. Interpretation, including misconfiguration and exposure assessment,
belongs to the AWS Cloud Security domain skill.

---

# Design Principles

The AWS Client Shared Skill SHALL be

- Deterministic in bounds given the same configuration and inputs
- Scope-confined to authorized accounts, regions, and services
- Provider-native — it exposes AWS resource models without abstracting them away
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

AWS Client Shared Skill

├── Service Connector       → HTTP Client (TLS)
├── Scope Confiner          (account · region · service)
├── Resource Describer      (describe · list · get)
├── Mutation Gatekeeper     → Policy Engine
├── IAM Inspector
├── Metadata Observer       (IMDS)
├── Pagination Bounder
├── Evidence Manager
├── Event Manager

↓

AWS Service APIs
```

The AWS Client performs operations but SHALL remain unaware of the API transport
implementation, which is provided by the HTTP and TLS shared skills.

---

# Responsibilities

The AWS Client Shared Skill is responsible for

- Connecting to AWS service endpoints via the [HTTP Client](../http-client/README.md)
- Authenticating via the [Authentication](../authentication/README.md) package and
  resolving credentials through the [Secrets Client](../secrets-client/README.md)
- Confining operations to authorized accounts, regions, and services
- Performing describe, list, and get operations and, where authorized, mutating
  operations
- Observing IAM, compute, network, and configuration metadata and reporting it as data
- Observing instance metadata service responses as data
- Applying rate and retry governance
- Emitting AWS lifecycle events and capturing evidence

---

# Operation Lifecycle

```
Receive Operation Request

↓

Acquire Rate Permit

↓

Confine To Authorized Scope (account · region · service)

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

The AWS Client SHALL confine operations to configured accounts, regions, and services.

A resource outside an authorized scope SHALL be rejected regardless of caller input.

Cross-account operations SHALL require explicit cross-account authorization.

---

# Read And Mutation Operations

The AWS Client SHALL support

- describe
- list
- get
- create
- update
- delete
- tag

`describe`, `list`, and `get` SHALL be read operations preferred by default.

`create`, `update`, `delete`, and `tag` SHALL be treated as intrusive and SHALL be
gated by the [Policy Engine](../policy-engine/README.md). Result sets and pagination
depth SHALL be bounded.

---

# IAM Observation

The AWS Client SHALL observe IAM principals, policies, and effective permissions, such
as through policy simulation and authorization-detail requests, and SHALL report them
as data.

Whether observed IAM represents an over-permissive condition SHALL be interpreted by
the domain skill, not this client.

---

# Instance Metadata Observation

The AWS Client SHALL observe the reachability and responses of the instance metadata
service (IMDS) and SHALL report them as data. Whether metadata reachability represents
a weakness SHALL be interpreted by the domain skill.

---

# Authentication

The AWS Client SHALL authenticate through the
[Authentication](../authentication/README.md) package, supporting

- access_key
- session_token
- assumed_role

Keys, tokens, and assumed-role credentials SHALL be resolved through the
[Secrets Client](../secrets-client/README.md) and SHALL NOT appear in evidence or logs.

---

# Governance

The AWS Client SHALL

- Acquire a permit from the [Rate Limiter](../rate-limiter/README.md) per operation
- Route through the [Proxy](../proxy/README.md) shared skill where configured
- Recover transient failures through the [Retry](../retry/README.md) shared skill

Mutations SHALL be gated as intrusive through the
[Policy Engine](../policy-engine/README.md).

---

# Evidence

The AWS Client Shared Skill SHOULD capture

- Account, region, and service identifiers
- Resource type and operation
- Result counts and pagination bounds
- Observed IAM, network, and configuration metadata
- Operation outcome

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain secrets,
credentials, or sensitive resource contents unless explicitly authorized and redacted.

---

# Events

The AWS Client Shared Skill SHOULD publish

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

The AWS Client Shared Skill depends on

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

The AWS Client Shared Skill SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- The AWS Cloud Security assessment skill
- Cloud asset-discovery skills enumerating AWS resources

---

# Outputs

Typical outputs MAY include

- Provider-native resource descriptions by reference
- IAM observation records
- Instance metadata observation records
- AWS evidence references

Outputs SHALL remain implementation independent while preserving AWS resource models.

---

# Security Principles

The AWS Client Shared Skill SHALL

- Confine access to authorized accounts, regions, and services
- Prefer read operations and gate mutations as intrusive
- Protect credentials from evidence and logs
- Report IAM, network, and configuration metadata as data, not findings
- Preserve auditability

AWS mutations can cause irreversible changes. The shared skill SHALL enforce
confinement and gate mutations through the Policy Engine.

---

# Best Practices

Consumers SHOULD

- Operate within the narrowest authorized account and region scope
- Prefer describe, list, and get
- Bound result sets and pagination depth
- Capture operation evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Call AWS service APIs directly
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
- adr/ADR-001-aws-service-abstraction.md

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

- [ADR-001 — AWS Service Abstraction](adr/ADR-001-aws-service-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Organization and control-tower awareness
- Config-recorder and inventory snapshots
- Cross-region aggregation descriptors
- Additional service coverage

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant AWS Client Shared Skill provides a confined, bounded, and
implementation-independent AWS service abstraction that preserves provider-native
resource models for the Robust PenTest Platform.

It enables consistent, auditable AWS interaction atop the HTTP and TLS shared skills
while enforcing scope and gating mutations, without embedding security interpretation
or API implementations in consumers.
