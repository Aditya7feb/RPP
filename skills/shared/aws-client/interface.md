# AWS Client Interface

**File:** `skills/shared/aws-client/interface.md`

**Version:** 1.0.0

---

# Purpose

The AWS Client Interface defines the canonical contract through which platform
components interact with AWS service and metadata endpoints.

The interface standardizes resource operations, scope confinement, mutation gating,
and result propagation while remaining independent of any API implementation and
preserving provider-native AWS resource models.

All consumers SHALL perform AWS access exclusively through this interface.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- API Independent
- Provider-Native
- Versioned
- Observable
- Backward Compatible
- Scope-Confined

---

# Relationship

```
Master Agent

↓

Cloud Security Domain Skill

↓

AWS Client Interface

↓

AWS Client Shared Skill

↓

HTTP Client (TLS) → AWS Service APIs
```

The interface SHALL NOT expose or depend on adapter internals.

---

# Interface Overview

```
Metadata

↓

Service Target

↓

Scope Reference

↓

Operation

↓

Governance References

↓

Execution Context

↓

Operation Result

↓

Evidence

↓

Errors
```

---

# Metadata

Every invocation SHALL include

```yaml
request_id:

assessment_id:

task_id:

skill_id:

timestamp:
```

Metadata enables tracing and auditing.

---

# Service Target

```yaml
service_target:
  account:
  region:
  service:
  endpoint_ref:
```

`service` SHALL name the AWS service. `endpoint_ref` MAY reference a resolved service
endpoint. Targets SHALL be within authorized scope.

---

# Scope Reference

```yaml
scope_ref:
  accounts:
  regions:
  services:
  cross_account_authorized:
```

The scope reference confines operations. Operations outside scope SHALL be rejected.

---

# Operation

```yaml
operation:
  kind: describe | list | get | create | update | delete | tag
  resource_type:
  selectors:
  pagination:
    max_items:
    max_pages:
```

`describe`, `list`, and `get` are read operations. `create`, `update`, `delete`, and
`tag` are intrusive and SHALL be gated through the Policy Engine.

---

# Governance References

```yaml
governance:
  rate_limit_ref:
  proxy_ref:
  retry_ref:
  policy_ref:
```

References bind the operation to governance shared skills.

---

# Operation Result

```yaml
operation_result:
  service:
  resource_type:
  items:
  item_count:
  iam_observations:
  metadata_observations:
  outcome: completed | partial | rejected | denied
```

`items` reference provider-native resource descriptions. `iam_observations` and
`metadata_observations` report observed data, never findings.

---

# Evidence

```yaml
evidence_ref:
```

The interface SHALL reference [Evidence](../../../schemas/evidence.md) capturing the
operation, redacting credentials and sensitive contents.

---

# Errors

Error categories are defined in [error-model.md](error-model.md). The interface SHALL
surface deterministic outcomes and SHALL NOT leak credentials or adapter internals.

---

# Interface Stability

Operations are stable. Additional read operations and resource types MAY be introduced
in a backward-compatible manner. Consumers SHALL ignore unknown result fields for
forward compatibility.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
