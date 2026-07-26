# Container Client Capabilities

**File:** `skills/shared/container-client/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Container Client Shared Skill.
Capabilities describe *what* the shared skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[Container Client Interface](interface.md).

---

# Capability Model

```
Connection

Scope

Read Operations

Mutation Operations

Configuration Observation

Governance

Observability
```

---

# Connection Capabilities

## Engine Connection

The Container Client SHALL connect to a container engine through the
[HTTP Client](../http-client/README.md) where an HTTP API is exposed.

---

## Authentication

The Container Client SHALL authenticate through the
[Authentication](../authentication/README.md) package.

---

# Scope Capabilities

## Scope Confinement

The Container Client SHALL confine operations to authorized engines, images, and containers.

---

# Read Operation Capabilities

## Inspect, List, And Get

The Container Client SHALL inspect, list, and get resources with bounded result sets and
inspection depth, preserving provider-native resource models.

---

## Image Layer Reading

The Container Client SHALL read image and layer contents through the
[Filesystem Client](../filesystem-client/README.md) only where authorized and bounded.

---

# Mutation Operation Capabilities

## Run, Exec, Stop, Remove

The Container Client SHALL perform mutations only with authorization.

---

## Workload Execution Gating

The Container Client SHALL require elevated authorization for run and exec operations.

---

## Intrusive Gating

The Container Client SHALL gate all mutations as intrusive through the
[Policy Engine](../policy-engine/README.md).

---

# Configuration Observation Capabilities

## Configuration Observation

The Container Client SHALL observe daemon, runtime, image, and container configuration and
report it as data.

---

# Governance Capabilities

## Rate And Proxy Governance

The Container Client SHALL apply rate and proxy governance through the
[Rate Limiter](../rate-limiter/README.md) and [Proxy](../proxy/README.md) shared skills.

---

## Retry Governance

The Container Client MAY retry transient failures through the
[Retry](../retry/README.md) shared skill.

---

# Observability Capabilities

## Evidence And Events

The Container Client SHALL capture evidence and publish lifecycle events conforming to
platform observability.

---

# Capability Boundaries

The Container Client SHALL NOT

- Produce findings or classify risk
- Interpret image, container, or configuration metadata as security posture
- Contain container-domain assessment logic
- Perform unauthorized mutations or workload execution

---

# Traceability

Each capability maps to interface operations in [interface.md](interface.md) and to
execution stages in [execution.md](execution.md).
