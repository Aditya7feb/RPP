# AWS Client Capabilities

**File:** `skills/shared/aws-client/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the AWS Client Shared Skill.
Capabilities describe *what* the shared skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[AWS Client Interface](interface.md).

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

The AWS Client SHALL connect to AWS service endpoints through the
[HTTP Client](../http-client/README.md) over TLS.

---

## Authentication

The AWS Client SHALL authenticate through the
[Authentication](../authentication/README.md) package.

---

# Scope Capabilities

## Scope Confinement

The AWS Client SHALL confine operations to authorized accounts, regions, and services.

---

## Cross-Account Authorization

The AWS Client SHALL require explicit authorization for cross-account operations.

---

# Read Operation Capabilities

## Describe, List, And Get

The AWS Client SHALL describe, list, and get resources with bounded result sets and
pagination depth, preserving provider-native resource models.

---

# Mutation Operation Capabilities

## Create, Update, Delete, Tag

The AWS Client SHALL perform mutations only with authorization.

---

## Intrusive Gating

The AWS Client SHALL gate all mutations as intrusive through the
[Policy Engine](../policy-engine/README.md).

---

# IAM Observation Capabilities

## IAM Observation

The AWS Client SHALL observe IAM principals, policies, and effective permissions and
report them as data.

---

# Metadata Observation Capabilities

## Instance Metadata Observation

The AWS Client SHALL observe instance metadata service reachability and responses and
report them as data.

---

# Governance Capabilities

## Rate And Proxy Governance

The AWS Client SHALL apply rate and proxy governance through the
[Rate Limiter](../rate-limiter/README.md) and [Proxy](../proxy/README.md) shared
skills.

---

## Retry Governance

The AWS Client MAY retry transient failures through the
[Retry](../retry/README.md) shared skill.

---

# Observability Capabilities

## Evidence And Events

The AWS Client SHALL capture evidence and publish lifecycle events conforming to
platform observability.

---

# Capability Boundaries

The AWS Client SHALL NOT

- Produce findings or classify risk
- Interpret IAM, network, or configuration metadata as security posture
- Contain cloud-domain assessment logic
- Perform unauthorized mutations or unbounded enumeration

---

# Traceability

Each capability maps to interface operations in [interface.md](interface.md) and to
execution stages in [execution.md](execution.md).
