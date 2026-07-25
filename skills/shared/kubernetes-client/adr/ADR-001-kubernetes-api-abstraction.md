# ADR-001 — Kubernetes API Abstraction

**File:** `skills/shared/kubernetes-client/adr/ADR-001-kubernetes-api-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform interacts with Kubernetes clusters to discover
cluster assets and assess configuration and posture. The Kubernetes API is a
large, versioned REST API over TLS, spanning many resource kinds, namespaces, and
verbs, including workload execution, and governed by RBAC.

If each skill called the Kubernetes API directly, the platform would suffer

- Duplicated API and transport logic
- Inconsistent or absent namespace and scope confinement
- Risk of unauthorized mutations or workload execution
- Risk of leaking tokens
- Divergent RBAC observation, evidence, and governance

The platform requires a single, canonical, implementation-independent Kubernetes
API abstraction that confines scope and gates mutations.

---

# Decision

The platform SHALL provide a dedicated Kubernetes Client shared skill that
centralizes cluster interaction behind a stable interface.

The Kubernetes Client shared skill SHALL

- Perform API requests through the [HTTP Client](../../http-client/README.md)
  over TLS, validating against a configured trust anchor
- Authenticate through the [Authentication](../../authentication/README.md)
  package and resolve tokens through the
  [Secrets Client](../../secrets-client/README.md)
- Confine operations to authorized namespaces and resource kinds
- Prefer read operations and gate mutations as intrusive, requiring elevated
  authorization for exec
- Observe RBAC and resource metadata and report it as data
- Produce evidence conforming to the
  [Evidence schema](../../../../schemas/evidence.md)

Consumers SHALL perform Kubernetes access exclusively through the
[Kubernetes Client Interface](../interface.md). The Kubernetes Client SHALL NOT
detect over-permissive RBAC or other misconfigurations; that interpretation
belongs to domain skills.

---

# Alternatives Considered

## Per-Skill API Access

Each skill could call the Kubernetes API directly.

Rejected because it duplicates logic and risks inconsistent confinement and
unauthorized mutation.

## Reimplementing HTTP And TLS

The client could implement its own transport.

Rejected because it would duplicate mature, governed handling already provided by
the HTTP and TLS shared skills, including proxy and interception awareness.

## Classifying RBAC In The Client

The client could classify over-permissive RBAC.

Rejected because finding generation belongs to domain skills. The client observes
and reports RBAC as data.

## Unrestricted Exec

Workload execution could be treated like any read.

Rejected because exec runs code in workloads and can cause irreversible effects.
Exec requires elevated, explicit authorization.

---

# Consequences

## Positive

- Uniform cluster interaction reusing HTTP and TLS handling
- Namespace and scope confinement enforced
- Mutations and exec gated as intrusive
- RBAC observed consistently as data
- Tokens protected and evidence consistent

## Negative

- Consumers MUST perform cluster access through the interface
- An additional shared dependency is introduced

The negative consequences are outweighed by safety and consistency.

---

# Compliance

Consumers SHALL

- Perform cluster access through the Kubernetes Client Interface
- Operate within authorized namespace scopes
- Prefer read operations
- Require elevated authorization for exec
- Interpret RBAC at the domain layer

---

# Future Compatibility

Future versions MAY add custom resource awareness, server-side apply, and
admission-review observation. These extensions SHALL preserve the existing
interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Kubernetes Client README](../README.md)
- [Kubernetes Client Interface](../interface.md)
- [Kubernetes Client Execution Model](../execution.md)
- [Kubernetes Client Error Model](../error-model.md)
- [HTTP Client](../../http-client/README.md)
- [Authentication](../../authentication/README.md)
- [Secrets Client](../../secrets-client/README.md)
- [Evidence Schema](../../../../schemas/evidence.md)
