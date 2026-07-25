# Kubernetes Client Capabilities

**File:** `skills/shared/kubernetes-client/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Kubernetes Client Shared
Skill. Capabilities describe *what* the shared skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[Kubernetes Client Interface](interface.md).

---

# Capability Model

```
Connection

Scope

Read Operations

Mutation Operations

RBAC Observation

Governance

Observability
```

---

# Connection Capabilities

## Cluster Connection

The Kubernetes Client SHALL connect to API servers through the
[HTTP Client](../http-client/README.md) over TLS.

---

## Authentication

The Kubernetes Client SHALL authenticate through the
[Authentication](../authentication/README.md) package.

---

# Scope Capabilities

## Scope Confinement

The Kubernetes Client SHALL confine operations to authorized namespaces and
resource kinds.

---

## Cluster-Scope Authorization

The Kubernetes Client SHALL require explicit authorization for cluster-scoped
operations.

---

# Read Operation Capabilities

## Get And List

The Kubernetes Client SHALL get and list resources with bounded result sets.

---

## Watch

The Kubernetes Client SHALL watch resources with bounded duration.

---

# Mutation Operation Capabilities

## Create, Update, Patch, Delete

The Kubernetes Client SHALL perform mutations with authorization.

---

## Exec Gating

The Kubernetes Client SHALL require elevated authorization for exec and attach
operations.

---

## Intrusive Gating

The Kubernetes Client SHALL gate all mutations and exec as intrusive.

---

# RBAC Observation Capabilities

## RBAC Observation

The Kubernetes Client SHALL observe effective permissions and report them as
data.

---

# Governance Capabilities

## Rate And Proxy Governance

The Kubernetes Client SHALL apply rate and proxy governance through the
[Rate Limiter](../rate-limiter/README.md) and [Proxy](../proxy/README.md) shared
skills.

---

## Retry Governance

The Kubernetes Client MAY retry transient failures through the
[Retry](../retry/README.md) shared skill.

---

# Observability Capabilities

## Evidence Capture

The Kubernetes Client SHOULD capture operation evidence conforming to the
[Evidence schema](../../../schemas/evidence.md).

---

## Event Emission

The Kubernetes Client SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The Kubernetes Client SHOULD expose metrics including operations, resources read,
resources mutated, and watch durations.

---

# Capability Boundaries

The Kubernetes Client SHALL NOT

- Detect over-permissive RBAC or other misconfigurations as findings
- Produce findings
- Access resources outside authorized scopes
- Perform unauthorized mutations or exec
- Persist tokens or sensitive resource contents

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Cluster Connection | Connection | SHALL |
| Authentication | Connection | SHALL |
| Scope Confinement | Scope | SHALL |
| Cluster-Scope Authorization | Scope | SHALL |
| Get And List | Read Operations | SHALL |
| Watch | Read Operations | SHALL |
| Create, Update, Patch, Delete | Mutation Operations | SHALL |
| Exec Gating | Mutation Operations | SHALL |
| Intrusive Gating | Mutation Operations | SHALL |
| RBAC Observation | RBAC Observation | SHALL |
| Rate And Proxy Governance | Governance | SHALL |
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
- [HTTP Client](../http-client/README.md)
