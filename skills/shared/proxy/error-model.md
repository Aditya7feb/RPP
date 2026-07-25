# Proxy Error Model

**File:** `skills/shared/proxy/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the Proxy Shared Skill.

The error model classifies the failure conditions the shared skill MAY produce
and aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The Proxy Shared Skill SHALL

- Produce canonical, structured errors
- Distinguish routing failures from governance rejections
- Preserve enough context for auditing
- Never leak proxy credentials

---

# Error Categories

The Proxy Shared Skill maps its failures onto the canonical categories.

```
Configuration

Validation

Connection

Authentication

Authorization

Governance

Adapter

Internal
```

---

# Configuration Errors

Raised when configuration is invalid or incomplete.

Conditions

- A proxy reference does not resolve
- `when_no_match` conflicts with `allow_direct_egress`
- A required credential reference is absent for an authenticated proxy

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when an invocation is malformed.

Conditions

- Missing destination fields
- Missing operation callback
- Invalid inline configuration override

Validation errors SHALL be non-retryable.

---

# Connection Errors

Raised when a proxy or tunnel cannot be established.

Conditions

- Proxy endpoint unreachable
- Tunnel negotiation failure
- Tunnel closed before the operation began

Connection errors MAY be retryable subject to the caller policy.

---

# Authentication Errors

Raised when proxy authentication fails.

Conditions

- Proxy rejects supplied credentials
- Credential resolution fails

Authentication errors SHALL NOT expose secret material and SHALL be
non-retryable without new credentials.

---

# Authorization Errors

Raised when the proxy refuses the destination.

Conditions

- Proxy policy forbids the destination
- Destination outside permitted egress

Authorization errors SHALL be non-retryable without policy change.

---

# Governance Errors

Raised when routing would violate platform governance.

Conditions

- Direct egress required but prohibited by `allow_direct_egress`
- A `require_proxy_schemes` destination has no available proxy

Governance errors SHALL be non-retryable without operator intervention.

---

# Adapter Errors

Raised when an underlying routing mechanism fails unexpectedly.

Adapter errors SHALL be normalized so that consumers remain unaware of the
implementation.

---

# Internal Errors

Raised for unexpected conditions within the Proxy Shared Skill.

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

proxy_id:

destination:
```

`category` SHALL be one of the canonical categories.

`retryable` SHALL indicate whether the operation MAY be attempted again.

Errors SHALL NOT contain secret material, including proxy credentials.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| proxy_unreachable | Connection | Policy dependent |
| tunnel_failed | Connection | Policy dependent |
| proxy_auth_failed | Authentication | No |
| destination_refused | Authorization | No |
| direct_egress_blocked | Governance | No |
| missing_proxy | Configuration | No |
| invalid_invocation | Validation | No |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# Interaction With Retry And Rate Limiter

A `Connection` error MAY be retried through the [Retry](../retry/README.md)
shared skill, and each retry SHOULD acquire a fresh permit from the
[Rate Limiter](../rate-limiter/README.md).

`Governance`, `Authorization`, and `Authentication` errors SHALL NOT be retried
automatically.

---

# Evidence

Errors SHOULD be captured as evidence conforming to the
[Evidence schema](../../../schemas/evidence.md), including the category, proxy
reference, and destination, and SHALL exclude credentials.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [Proxy Configuration Schema](../../../schemas/proxy-configuration.md)
