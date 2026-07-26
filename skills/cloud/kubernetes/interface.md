# Kubernetes Cloud Security Skill Interface

**File:** `skills/cloud/kubernetes/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Kubernetes
Cloud Security Skill. The interface describes intent, not the Kubernetes API or tooling.

---

# Interface Overview

The skill exposes a single logical operation, `assess`, that evaluates Kubernetes cluster
security posture for an in-scope cluster and returns Findings with Evidence references.

---

# Operation: assess

## Request

```yaml
assess:
  target:
  assets:
  namespace_scope_ref:
  credential_ref:
  scope_id:
  roe_id:
  options:
    check_rbac:
    check_workloads:
    check_exposure:
    check_network_policy:
    check_secrets:
```

`target` SHALL be an in-scope Kubernetes cluster. `assets` reference `cloud-resource`
[Assets](../../../schemas/asset.md). `namespace_scope_ref` references authorized namespaces
and resource kinds. `credential_ref` references authorized read credentials by reference
only. `options` toggle individual analyses and default to configuration defaults.

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
- No out-of-scope namespace SHALL have been assessed.
- The cluster SHALL NOT have been mutated and no workload SHALL have been executed.

---

# Error Semantics

Error categories and outcomes are defined in [error-model.md](error-model.md). The
interface SHALL surface deterministic outcomes and SHALL NOT leak credentials or API
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
