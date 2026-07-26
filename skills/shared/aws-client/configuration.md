# AWS Client Configuration

**File:** `skills/shared/aws-client/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the AWS Client Shared Skill and
the precedence rules that govern it. Configuration describes structure and intent only.

---

# Configuration Object

```yaml
aws_client:
  scope:
    accounts:
    regions:
    services:
    cross_account_authorized: false

  operations:
    read_preferred: true
    mutations_enabled: false

  pagination:
    max_items:
    max_pages:

  metadata:
    observe_imds: true

  authentication:
    method: access_key | session_token | assumed_role
    secret_ref:

  governance:
    rate_limit_ref:
    proxy_ref:
    retry_ref:
    policy_ref:

  evidence:
    redact_secrets: true
    capture_metadata: true
```

---

# Field Definitions

## scope

`accounts`, `regions`, and `services` enumerate authorized scope. `cross_account_authorized`
SHALL default to `false`. Operations outside scope SHALL be rejected.

## operations

`read_preferred` SHALL default to `true`. `mutations_enabled` SHALL default to `false`;
when enabled, mutations remain gated by the Policy Engine.

## pagination

`max_items` and `max_pages` bound enumeration. The client SHALL NOT exceed these bounds.

## metadata

`observe_imds` enables observation of the instance metadata service; observations are
reported as data.

## authentication

`method` selects the credential type. `secret_ref` references credentials resolved
through the [Secrets Client](../secrets-client/README.md). Credentials SHALL NOT appear
inline.

## governance

Governance references bind rate limiting, proxying, retry, and policy enforcement.

## evidence

`redact_secrets` SHALL default to `true`. `capture_metadata` controls whether observed
metadata is captured as evidence.

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

- `accounts`, `regions`, and `services` SHALL be non-empty for active operations.
- `max_items` and `max_pages` SHALL be positive integers when present.
- `secret_ref` SHALL be present when a target requires authentication.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
