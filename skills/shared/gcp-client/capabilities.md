# GCP Client Capabilities

**File:** `skills/shared/gcp-client/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the GCP Client Shared Skill.
Capabilities describe *what* the shared skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[GCP Client Interface](interface.md).

---

# Capability Model

```
Connection

Scope

Read Operations

Mutation Operations

IAM Observation

Metadata Observation

Governance

Observability
```

---

# Connection Capabilities

## Service Connection

The GCP Client SHALL connect to GCP service endpoints through the
[HTTP Client](../http-client/README.md) over TLS.

---

## Authentication

The GCP Client SHALL authenticate through the
[Authentication](../authentication/README.md) package.

---

# Scope Capabilities

## Scope Confinement

The GCP Client SHALL confine operations to authorized organizations, projects, regions,
and services.

---

## Cross-Project Authorization

The GCP Client SHALL require explicit authorization for cross-project operations.

---

# Read Operation Capabilities

## Get And List

The GCP Client SHALL get and list resources with bounded result sets and pagination depth,
preserving provider-native resource models.

---

# Mutation Operation Capabilities

## Create, Update, Delete, Set-IAM-Policy

The GCP Client SHALL perform mutations only with authorization.

---

## Intrusive Gating

The GCP Client SHALL gate all mutations as intrusive through the
[Policy Engine](../policy-engine/README.md).

---

# IAM Observation Capabilities

## IAM Observation

The GCP Client SHALL observe IAM policy bindings and effective permissions and report them
as data.

---

# Metadata Observation Capabilities

## Metadata Server Observation

The GCP Client SHALL observe metadata server reachability and responses and report them as
data.

---

# Governance Capabilities

## Rate And Proxy Governance

The GCP Client SHALL apply rate and proxy governance through the
[Rate Limiter](../rate-limiter/README.md) and [Proxy](../proxy/README.md) shared skills.

---

## Retry Governance

The GCP Client MAY retry transient failures through the
[Retry](../retry/README.md) shared skill.

---

# Observability Capabilities

## Evidence And Events

The GCP Client SHALL capture evidence and publish lifecycle events conforming to platform
observability.

---

# Capability Boundaries

The GCP Client SHALL NOT

- Produce findings or classify risk
- Interpret IAM, network, or configuration metadata as security posture
- Contain cloud-domain assessment logic
- Perform unauthorized mutations or unbounded enumeration

---

# Traceability

Each capability maps to interface operations in [interface.md](interface.md) and to
execution stages in [execution.md](execution.md).
