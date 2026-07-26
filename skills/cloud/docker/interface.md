# Docker Cloud Security Skill Interface

**File:** `skills/cloud/docker/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Docker Cloud
Security Skill. The interface describes intent, not the container engine or tooling.

---

# Interface Overview

The skill exposes a single logical operation, `assess`, that evaluates container platform
security posture for an in-scope platform and returns Findings with Evidence references.

---

# Operation: assess

## Request

```yaml
assess:
  target:
  assets:
  engine_scope_ref:
  credential_ref:
  scope_id:
  roe_id:
  options:
    check_privilege:
    check_host_exposure:
    check_insecure_defaults:
    check_resource_limits:
    check_secrets:
```

`target` SHALL be an in-scope container platform. `assets` reference `cloud-resource`
[Assets](../../../schemas/asset.md). `engine_scope_ref` references authorized engines,
images, and containers. `credential_ref` references authorized read credentials by
reference only. `options` toggle individual analyses and default to configuration defaults.

## Response

```yaml
assess_result:
  target:
  findings:
  evidence_refs:
  observations:
  assets:
  decision_summary:
```

`findings` reference [Finding](../../../schemas/finding.md) objects, each with
[Risk](../../../schemas/risk.md). `assets` reference enriched `cloud-resource` Assets.
`decision_summary` summarizes Policy Engine decisions.

---

# Preconditions

- `target` SHALL be within the assessment [Scope](../../../schemas/scope.md).
- The [Policy Engine](../../shared/policy-engine/README.md) SHALL be available.
- `credential_ref` SHALL reference authorized read credentials.

---

# Postconditions

- Every returned Finding SHALL reference supporting Evidence.
- No out-of-scope engine SHALL have been assessed.
- The platform SHALL NOT have been mutated and no container SHALL have been executed.

---

# Error Semantics

Error categories and outcomes are defined in [error-model.md](error-model.md). The
interface SHALL surface deterministic outcomes and SHALL NOT leak credentials or engine
internals.

---

# Interface Stability

The `assess` operation is stable. Additional options MAY be introduced in a
backward-compatible manner. Consumers SHALL ignore unknown response fields for forward
compatibility.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
