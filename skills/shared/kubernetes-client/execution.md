# Kubernetes Client Execution Model

**File:** `skills/shared/kubernetes-client/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the Kubernetes Client Shared Skill.

The execution model describes how the shared skill performs an API operation from
scope confinement through mutation gating, the operation itself, and RBAC
observation.

The model is deterministic in bounds given the same configuration and inputs.

---

# Execution Overview

```
Receive Operation Request

↓

Resolve Configuration

↓

Acquire Rate Permit

↓

Confine To Authorized Scope

↓

Connect And Authenticate (HTTP Client, TLS)

↓

Gate Mutations / Exec

↓

Perform Operation (bounded, authorized)

↓

Observe RBAC / Metadata

↓

Emit Evidence and Events

↓

Return Result
```

---

# Stage 1 — Configuration Resolution

The Kubernetes Client SHALL resolve clusters, scopes, execution gating, and
bounds using the precedence defined in [configuration.md](configuration.md).

Scope confinement and mutation gating SHALL always be enforced.

---

# Stage 2 — Rate Permit

The Kubernetes Client SHALL acquire a permit from the
[Rate Limiter](../rate-limiter/README.md) for the operation.

---

# Stage 3 — Scope Confinement

The Kubernetes Client SHALL confine the operation to an authorized namespace and
resource kind.

A resource outside the scope SHALL be rejected with `scope_rejected`.

Cluster-scoped operations SHALL proceed only when `cluster_scoped` is authorized.

---

# Stage 4 — Connect And Authenticate

The Kubernetes Client SHALL connect to the API server through the
[HTTP Client](../http-client/README.md) over TLS, validating against the
configured trust anchor, and authenticate through the
[Authentication](../authentication/README.md) package.

Tokens SHALL be resolved through the [Secrets Client](../secrets-client/README.md)
and SHALL NOT appear in evidence.

---

# Stage 5 — Mutation Gating

`create`, `update`, `patch`, and `delete` SHALL proceed only when
`allow_mutations` is enabled.

`exec` and `attach` SHALL proceed only when `allow_exec` is enabled, requiring
elevated authorization because they execute in workloads.

Unauthorized intrusive operations SHALL be rejected.

---

# Stage 6 — Operation

The Kubernetes Client SHALL perform the operation bounded by configured limits.

- `get` SHALL return a single object, referenced when large
- `list` SHALL bound items by `max_items`
- `watch` SHALL bound duration by `watch_duration`
- mutating verbs SHALL apply the referenced body when authorized
- `exec` SHALL bound session duration and output

The Kubernetes Client SHALL NOT interpret resource contents as findings.

---

# Stage 7 — RBAC Observation

The Kubernetes Client SHALL observe effective permissions, such as through
access-review requests, and SHALL report them as data.

The client SHALL NOT classify RBAC as over-permissive.

---

# Stage 8 — Evidence And Events

The Kubernetes Client SHOULD emit operation evidence and lifecycle events
according to configuration. Evidence SHALL exclude tokens and sensitive contents.

---

# Retry Behavior

Transient failures MAY be retried through the [Retry](../retry/README.md) shared
skill, each retry acquiring a fresh permit.

Mutations SHALL be retried only when idempotent and authorized; `exec` SHALL NOT
be retried automatically.

---

# Determinism

Given identical configuration and inputs, the Kubernetes Client SHALL enforce
identical confinement and bounds and produce identical outcome classifications
for the same observed cluster state.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A scope violation SHALL never perform the operation.

An API `403` SHALL map to a `forbidden` outcome preserving the reason.

---

# Execution Outputs

The execution model SHALL produce

- Resource listings and objects by reference
- RBAC observation records
- Bounded watch event streams
- Operation metrics
- Evidence references

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [HTTP Client](../http-client/README.md)
- [Secrets Client](../secrets-client/README.md)
- [Execution Model](../../core/execution-model.md)
