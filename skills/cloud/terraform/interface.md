# Terraform Cloud Security Skill Interface

**File:** `skills/cloud/terraform/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Terraform
Cloud Security Skill. The interface describes intent, not Terraform tooling.

---

# Interface Overview

The skill exposes a single logical operation, `assess`, that statically evaluates Terraform
configuration for an in-scope source and returns Findings with Evidence references.

---

# Operation: assess

## Request

```yaml
assess:
  target:
  assets:
  configuration_root_ref:
  scope_id:
  roe_id:
  options:
    check_resource_config:
    check_public_exposure:
    check_encryption:
    check_access:
    check_secrets:
```

`target` SHALL be an in-scope Terraform configuration source. `assets` reference
`repository` or `cloud-resource` [Assets](../../../schemas/asset.md).
`configuration_root_ref` references the authorized filesystem root. `options` toggle
individual analyses and default to configuration defaults.

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
- `configuration_root_ref` SHALL reference an authorized filesystem root.

---

# Postconditions

- Every returned Finding SHALL reference supporting Evidence.
- No out-of-scope configuration root SHALL have been read.
- No infrastructure SHALL have been provisioned, planned, or applied.

---

# Error Semantics

Error categories and outcomes are defined in [error-model.md](error-model.md). The interface
SHALL surface deterministic outcomes and SHALL NOT leak secrets or tooling internals.

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
