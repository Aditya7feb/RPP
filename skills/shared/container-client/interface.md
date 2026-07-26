# Container Client Interface

**File:** `skills/shared/container-client/interface.md`

**Version:** 1.0.0

---

# Purpose

The Container Client Interface defines the canonical contract through which platform
components interact with container engines and their resources.

The interface standardizes resource operations, scope confinement, mutation gating, and
result propagation while remaining independent of any engine implementation and preserving
provider-native container resource models.

All consumers SHALL perform container-engine access exclusively through this interface.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- Engine Independent
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

Container Client Interface

↓

Container Client Shared Skill

↓

HTTP Client (TLS) / Filesystem Client → Container Engine API
```

The interface SHALL NOT expose or depend on adapter internals.

---

# Interface Overview

```
Metadata

↓

Engine Target

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

# Engine Target

```yaml
engine_target:
  engine:
  endpoint_ref:
```

`engine` SHALL identify the container engine. `endpoint_ref` MAY reference a resolved engine
endpoint. Targets SHALL be within authorized scope.

---

# Scope Reference

```yaml
scope_ref:
  engines:
  images:
  containers:
```

The scope reference confines operations. Operations outside scope SHALL be rejected.

---

# Operation

```yaml
operation:
  kind: inspect | list | get | run | exec | stop | remove
  resource_type:
  selectors:
  bounds:
    max_items:
    max_depth:
```

`inspect`, `list`, and `get` are read operations. `run`, `exec`, `stop`, and `remove` are
intrusive and SHALL be gated through the Policy Engine, with `run` and `exec` requiring
elevated authorization.

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
  engine:
  resource_type:
  items:
  item_count:
  config_observations:
  outcome: completed | partial | rejected | denied
```

`items` reference provider-native resource descriptions. `config_observations` report
observed data, never findings.

---

# Evidence

```yaml
evidence_ref:
```

The interface SHALL reference [Evidence](../../../schemas/evidence.md) capturing the
operation, redacting credentials and sensitive contents.

---

# Errors

Error categories are defined in [error-model.md](error-model.md). The interface SHALL surface
deterministic outcomes and SHALL NOT leak credentials or adapter internals.

---

# Interface Stability

Operations are stable. Additional read operations and resource types MAY be introduced in a
backward-compatible manner. Consumers SHALL ignore unknown result fields for forward
compatibility.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
