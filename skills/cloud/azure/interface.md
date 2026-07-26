# Azure Cloud Security Skill Interface

**File:** `skills/cloud/azure/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Azure Cloud
Security Skill. The interface describes intent, not provider APIs or tooling.

---

# Interface Overview

The skill exposes a single logical operation, `assess`, that evaluates Azure security
posture for an in-scope environment and returns Findings with Evidence references.

---

# Operation: assess

## Request

```yaml
assess:
  target:
  assets:
  subscription_scope_ref:
  credential_ref:
  scope_id:
  roe_id:
  options:
    check_roles:
    check_public_exposure:
    check_network_exposure:
    check_encryption:
    check_insecure_defaults:
```

`target` SHALL be an in-scope Azure environment. `assets` reference `cloud-resource`
[Assets](../../../schemas/asset.md). `subscription_scope_ref` references authorized
subscriptions, resource groups, regions, and services. `credential_ref` references
authorized read credentials by reference only. `options` toggle individual analyses and
default to configuration defaults.

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
- No out-of-scope subscription SHALL have been assessed.
- The environment SHALL NOT have been mutated.

---

# Error Semantics

Error categories and outcomes are defined in [error-model.md](error-model.md). The
interface SHALL surface deterministic outcomes and SHALL NOT leak credentials or provider
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
