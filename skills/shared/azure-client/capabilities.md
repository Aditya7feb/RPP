# Azure Client Capabilities

**File:** `skills/shared/azure-client/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Azure Client Shared Skill.
Capabilities describe *what* the shared skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[Azure Client Interface](interface.md).

---

# Capability Model

```
Connection

Scope

Read Operations

Mutation Operations

Role Observation

Metadata Observation

Governance

Observability
```

---

# Connection Capabilities

## Service Connection

The Azure Client SHALL connect to Azure service endpoints through the
[HTTP Client](../http-client/README.md) over TLS.

---

## Authentication

The Azure Client SHALL authenticate through the
[Authentication](../authentication/README.md) package.

---

# Scope Capabilities

## Scope Confinement

The Azure Client SHALL confine operations to authorized subscriptions, resource groups,
regions, and services.

---

## Cross-Subscription Authorization

The Azure Client SHALL require explicit authorization for cross-subscription operations.

---

# Read Operation Capabilities

## Get And List

The Azure Client SHALL get and list resources with bounded result sets and pagination
depth, preserving provider-native resource models.

---

# Mutation Operation Capabilities

## Create, Update, Delete, Tag

The Azure Client SHALL perform mutations only with authorization.

---

## Intrusive Gating

The Azure Client SHALL gate all mutations as intrusive through the
[Policy Engine](../policy-engine/README.md).

---

# Role Observation Capabilities

## Role Observation

The Azure Client SHALL observe Entra ID role assignments and effective permissions and
report them as data.

---

# Metadata Observation Capabilities

## Instance Metadata Observation

The Azure Client SHALL observe Azure Instance Metadata Service reachability and responses
and report them as data.

---

# Governance Capabilities

## Rate And Proxy Governance

The Azure Client SHALL apply rate and proxy governance through the
[Rate Limiter](../rate-limiter/README.md) and [Proxy](../proxy/README.md) shared skills.

---

## Retry Governance

The Azure Client MAY retry transient failures through the
[Retry](../retry/README.md) shared skill.

---

# Observability Capabilities

## Evidence And Events

The Azure Client SHALL capture evidence and publish lifecycle events conforming to
platform observability.

---

# Capability Boundaries

The Azure Client SHALL NOT

- Produce findings or classify risk
- Interpret role, network, or configuration metadata as security posture
- Contain cloud-domain assessment logic
- Perform unauthorized mutations or unbounded enumeration

---

# Traceability

Each capability maps to interface operations in [interface.md](interface.md) and to
execution stages in [execution.md](execution.md).
