# Kubernetes Client Error Model

**File:** `skills/shared/kubernetes-client/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the Kubernetes Client Shared Skill.

The error model classifies the failure conditions the shared skill MAY produce
and aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The Kubernetes Client Shared Skill SHALL

- Produce canonical, structured errors
- Enforce scope confinement and mutation gating as boundaries
- Preserve API reasons for domain interpretation
- Never leak tokens or sensitive resource contents

---

# Error Categories

The Kubernetes Client maps its failures onto the canonical categories.

```
Configuration

Validation

Connection

Scope

Authentication

Authorization

NotFound

Timeout

Governance

Adapter

Internal
```

---

# Configuration Errors

Raised when configuration is invalid.

Conditions

- A referenced cluster or scope does not exist
- A scope references a missing cluster
- A referenced default policy does not resolve

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when an invocation is malformed.

Conditions

- Missing cluster, scope, or resource identifiers
- Inline token supplied
- A mutating verb without authorization

Validation errors SHALL be non-retryable.

---

# Connection Errors

Raised when the API server cannot be reached or TLS validation fails.

Connection errors SHALL propagate the canonical
[HTTP Client](../http-client/README.md) or
[TLS Client](../tls-client/README.md) error and MAY be retryable when transient.

---

# Scope Errors

Raised when a resource escapes an authorized scope.

Scope errors SHALL be non-retryable and SHALL preserve the attempted scope for
audit without performing the operation.

---

# Authentication Errors

Raised when cluster authentication fails.

Authentication errors SHALL NOT expose tokens and SHALL be non-retryable without
new credentials.

---

# Authorization Errors

Raised when the API server denies the operation.

Conditions

- API `403` forbidden

Authorization errors SHALL map to a `forbidden` outcome, preserve the API reason
as data, and SHALL NOT be classified as findings.

---

# Not-Found Errors

Raised when a resource does not exist.

Not-found errors SHALL be distinguished from scope rejections and MAY be expected
during discovery.

---

# Timeout Errors

Raised when a bound is exceeded.

Conditions

- Request timeout
- Watch duration exceeded

Timeout errors SHALL carry the breached bound.

---

# Governance Errors

Raised when an operation would violate governance.

Conditions

- Mutation attempted when `allow_mutations` is disabled
- Exec attempted when `allow_exec` is disabled
- Cluster-scoped operation without authorization
- Rate ceiling exceeded

Governance errors SHALL be non-retryable without operator intervention.

---

# Adapter Errors

Raised when an underlying API adapter fails unexpectedly.

Adapter errors SHALL be normalized so that consumers remain unaware of the
implementation.

---

# Internal Errors

Raised for unexpected conditions within the Kubernetes Client.

Internal errors SHALL be treated as non-retryable and SHOULD be reported for
diagnosis.

---

# Error Structure

Every error SHALL conform to the canonical error structure.

```yaml
category:

code:

message:

retryable:

cluster_id:

namespace:

reason:
```

`category` SHALL be one of the canonical categories.

`reason` SHALL carry the API reason where applicable.

`retryable` SHALL indicate whether the operation MAY be attempted again.

Errors SHALL NOT contain tokens or sensitive resource contents.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| connect_failed | Connection | Transient only |
| scope_rejected | Scope | No |
| auth_failed | Authentication | No |
| forbidden | Authorization | No |
| not_found | NotFound | Context dependent |
| mutation_blocked | Governance | No |
| exec_blocked | Governance | No |
| timed_out | Timeout | No |
| rejected | Governance | No |
| invalid_request | Validation | No |
| missing_cluster | Configuration | No |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# Confinement Principle

The Kubernetes Client SHALL never perform an operation on a resource outside an
authorized scope, and SHALL never perform a mutation or exec without explicit
authorization.

Violations SHALL be rejected and preserved for audit rather than silently
performed.

---

# Evidence

Errors SHOULD be captured as evidence conforming to the
[Evidence schema](../../../schemas/evidence.md), including the category, cluster,
namespace, and API reason, and SHALL exclude tokens and sensitive contents.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [HTTP Client](../http-client/README.md)
