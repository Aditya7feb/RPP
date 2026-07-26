# Container Client Configuration

**File:** `skills/shared/container-client/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Container Client Shared Skill and
the precedence rules that govern it. Configuration describes structure and intent only.

---

# Configuration Object

```yaml
container_client:
  scope:
    engines:
    images:
    containers:

  operations:
    read_preferred: true
    mutations_enabled: false
    workload_execution_enabled: false

  bounds:
    max_items:
    max_depth:

  authentication:
    method: client_certificate | bearer_token | registry_credential
    secret_ref:

  governance:
    rate_limit_ref:
    proxy_ref:
    retry_ref:
    policy_ref:

  evidence:
    redact_secrets: true
    capture_config: true
```

---

# Field Definitions

## scope

`engines`, `images`, and `containers` enumerate authorized scope. Operations outside scope
SHALL be rejected.

## operations

`read_preferred` SHALL default to `true`. `mutations_enabled` and
`workload_execution_enabled` SHALL default to `false`; when enabled, mutations and workload
execution remain gated by the Policy Engine, with run and exec requiring elevated
authorization.

## bounds

`max_items` and `max_depth` bound enumeration and inspection depth. The client SHALL NOT
exceed these bounds.

## authentication

`method` selects the credential type. `secret_ref` references credentials resolved through
the [Secrets Client](../secrets-client/README.md). Credentials SHALL NOT appear inline.

## governance

Governance references bind rate limiting, proxying, retry, and policy enforcement.

## evidence

`redact_secrets` SHALL default to `true`. `capture_config` controls whether observed
configuration is captured as evidence.

---

# Precedence

Configuration precedence, from highest to lowest, SHALL be

1. Scope and authorization constraints
2. Policy Engine decisions
3. Per-operation parameters
4. Shared-skill configuration in this document
5. Documented defaults

A more permissive configuration SHALL NOT override a more restrictive scope or policy
decision.

---

# Validation Rules

- `engines` SHALL be non-empty for active operations.
- `max_items` and `max_depth` SHALL be positive integers when present.
- `secret_ref` SHALL be present when an engine requires authentication.
- `workload_execution_enabled` SHALL require elevated authorization to take effect.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
