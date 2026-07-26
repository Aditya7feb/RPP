# Container Client Shared Skill

**File:** `skills/shared/container-client/README.md`

**Version:** 1.0.0

---

# Purpose

The Container Client Shared Skill provides the canonical, implementation-independent
mechanism for interacting with container engines and their images, containers, and
configuration within the Robust PenTest Platform (RPP).

Rather than allowing individual skills to call a container engine directly, this shared
skill centralizes engine access, image and container inspection, mutation gating,
configuration observation, and observability behind a stable interface exposing
provider-native container resource models.

All packages that require container-engine access SHALL delegate to this shared skill.

---

# Goals

The Container Client Shared Skill SHALL

- Abstract container-engine access behind a stable, provider-native interface
- Perform engine requests through the [HTTP Client](../http-client/README.md) where the
  engine exposes an HTTP API
- Inspect image and layer contents through the [Filesystem Client](../filesystem-client/README.md)
  where authorized
- Authenticate through the [Authentication](../authentication/README.md) package
- Confine operations to authorized engines, images, and containers
- Prefer read operations (inspect, list, get) and gate mutations as intrusive
- Observe image, container, network, and daemon configuration metadata and report it as
  data
- Produce container evidence
- Integrate with platform observability

---

# Non-Goals

The Container Client Shared Skill SHALL NOT

- Detect vulnerabilities such as privileged containers or exposed daemons
- Produce security findings
- Classify risk
- Interpret image, container, or configuration metadata as security posture
- Contain container-domain assessment logic
- Perform mutations without authorization
- Execute workloads implicitly

The Container Client performs confined, authorized engine access and reports provider-native
metadata as data. Interpretation, including misconfiguration assessment, belongs to the
Docker Cloud Security domain skill.

---

# Design Principles

The Container Client Shared Skill SHALL be

- Deterministic in bounds given the same configuration and inputs
- Scope-confined to authorized engines, images, and containers
- Provider-native — it exposes container resource models without abstracting them away
- Read-preferring with explicit mutation gating
- Bounded in result size and inspection depth
- Governed
- Secure by default

---

# Architecture

```
Master Agent

↓

Cloud Security Domain Skill

↓

Container Client Shared Skill

├── Engine Connector        → HTTP Client (TLS) / local endpoint
├── Scope Confiner          (engine · image · container)
├── Resource Inspector      (inspect · list · get)
├── Image Layer Reader      → Filesystem Client
├── Mutation Gatekeeper     → Policy Engine
├── Config Observer         (daemon · runtime)
├── Evidence Manager
├── Event Manager

↓

Container Engine API
```

The Container Client performs operations but SHALL remain unaware of the engine transport
implementation, which is provided by the HTTP, TLS, and Filesystem shared skills.

---

# Responsibilities

The Container Client Shared Skill is responsible for

- Connecting to a container engine via the [HTTP Client](../http-client/README.md) where an
  HTTP API is exposed
- Authenticating via the [Authentication](../authentication/README.md) package and resolving
  credentials through the [Secrets Client](../secrets-client/README.md)
- Confining operations to authorized engines, images, and containers
- Performing inspect, list, and get operations and, where authorized, mutating operations
- Reading image and layer contents through the [Filesystem Client](../filesystem-client/README.md)
  where authorized
- Observing image, container, network, and daemon configuration metadata and reporting it as
  data
- Applying rate and retry governance
- Emitting container lifecycle events and capturing evidence

---

# Operation Lifecycle

```
Receive Operation Request

↓

Acquire Rate Permit

↓

Confine To Authorized Scope (engine · image · container)

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

The Container Client SHALL confine operations to configured engines, images, and containers.

A resource outside an authorized scope SHALL be rejected regardless of caller input.

Access to the engine or host beyond authorized scope SHALL be rejected.

---

# Read And Mutation Operations

The Container Client SHALL support

- inspect
- list
- get
- run
- exec
- stop
- remove

`inspect`, `list`, and `get` SHALL be read operations preferred by default.

`run`, `exec`, `stop`, and `remove` SHALL be treated as intrusive and SHALL be gated by the
[Policy Engine](../policy-engine/README.md). `run` and `exec` SHALL require elevated,
explicit authorization because they execute workloads. Result sets and inspection depth
SHALL be bounded.

---

# Configuration Observation

The Container Client SHALL observe daemon and runtime configuration, image manifests, and
container settings and SHALL report them as data.

Whether observed configuration represents a weakness, such as a privileged container or an
exposed daemon socket, SHALL be interpreted by the domain skill, not this client.

---

# Authentication

The Container Client SHALL authenticate through the
[Authentication](../authentication/README.md) package, supporting

- client_certificate
- bearer_token
- registry_credential

Credentials SHALL be resolved through the [Secrets Client](../secrets-client/README.md) and
SHALL NOT appear in evidence or logs.

---

# Governance

The Container Client SHALL

- Acquire a permit from the [Rate Limiter](../rate-limiter/README.md) per operation
- Route through the [Proxy](../proxy/README.md) shared skill where configured
- Recover transient failures through the [Retry](../retry/README.md) shared skill

Mutations and workload execution SHALL be gated as intrusive through the
[Policy Engine](../policy-engine/README.md).

---

# Evidence

The Container Client Shared Skill SHOULD capture

- Engine, image, and container identifiers
- Resource type and operation
- Result counts and inspection bounds
- Observed image, container, and configuration metadata
- Operation outcome

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain secrets, credentials,
or sensitive image contents unless explicitly authorized and redacted.

---

# Events

The Container Client Shared Skill SHOULD publish

- EngineConnected
- ScopeConfined
- ResourceInspected
- ResourceMutated
- ConfigObserved
- WorkloadExecuted
- OperationFailed

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The Container Client Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [HTTP Client](../http-client/README.md)
- [Filesystem Client](../filesystem-client/README.md)
- [Authentication](../authentication/README.md)
- [Secrets Client](../secrets-client/README.md)
- [Policy Engine](../policy-engine/README.md)
- [Proxy](../proxy/README.md)
- [Rate Limiter](../rate-limiter/README.md)
- [Retry](../retry/README.md)
- [Evidence Schema](../../../schemas/evidence.md)

The Container Client Shared Skill SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- The Docker Cloud Security assessment skill
- Container-platform review skills

---

# Outputs

Typical outputs MAY include

- Provider-native image and container descriptions by reference
- Configuration observation records
- Container evidence references

Outputs SHALL remain implementation independent while preserving container resource models.

---

# Security Principles

The Container Client Shared Skill SHALL

- Confine access to authorized engines, images, and containers
- Prefer read operations and gate mutations as intrusive
- Require elevated authorization for workload execution
- Protect credentials from evidence and logs
- Report image, container, and configuration metadata as data, not findings
- Preserve auditability

Container mutations and workload execution can cause irreversible changes. The shared skill
SHALL enforce confinement and gate mutations through the Policy Engine.

---

# Best Practices

Consumers SHOULD

- Operate within the narrowest authorized engine and image scope
- Prefer inspect, list, and get
- Require elevated authorization for run and exec
- Bound result sets and inspection depth
- Capture operation evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Call the container engine directly
- Access resources outside authorized scopes
- Perform unauthorized mutations or workload execution
- Interpret configuration as findings within the transport layer
- Persist credentials or sensitive image contents in evidence

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
- adr/ADR-001-container-engine-abstraction.md

---

# Related Shared Packages

- [HTTP Client](../http-client/README.md)
- [Filesystem Client](../filesystem-client/README.md)
- [Authentication](../authentication/README.md)
- [Secrets Client](../secrets-client/README.md)
- [Kubernetes Client](../kubernetes-client/README.md)
- [Policy Engine](../policy-engine/README.md)

---

# Canonical Schemas

- [Evidence](../../../schemas/evidence.md)
- [HTTP Transaction](../../../schemas/http-transaction.md)

---

# Architecture Decisions

- [ADR-001 — Container Engine Abstraction](adr/ADR-001-container-engine-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Image signature and provenance descriptors
- Runtime security-profile observation
- Registry inventory enumeration
- Additional engine coverage

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Container Client Shared Skill provides a confined, bounded, and
implementation-independent container-engine abstraction that preserves provider-native
resource models for the Robust PenTest Platform.

It enables consistent, auditable container interaction atop the HTTP, TLS, and Filesystem
shared skills while enforcing scope and gating mutations, without embedding security
interpretation or engine implementations in consumers.
