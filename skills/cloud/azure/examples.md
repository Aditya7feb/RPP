# Azure Cloud Security Skill Examples

**File:** `skills/cloud/azure/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Azure Cloud
Security Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — Publicly Accessible Storage Account

## Request

```yaml
target: azure-subscription-00000000-0000-0000-0000-000000000000
assets:
  - asset-cloud-6101
subscription_scope_ref: azure-scope-example
credential_ref: azure-read-credential
scope_id: scope-example-2024
roe_id: roe-example-2024
options:
  check_public_exposure: true
```

## Result

```yaml
findings:
  - id: finding-azure-5001
    title: Storage account container is publicly accessible
    weakness: CWE-284
    benchmark: CIS Azure Foundations - storage public access
    asset: asset-cloud-6101
    risk_ref: risk-azure-3001
    evidence_refs:
      - evidence-azure-7001
observations:
  - id: obs-azure-4001
    kind: public-exposure-analysis
evidence:
  - id: evidence-azure-7001
    observation_ref: obs-azure-4001
status: completed
metrics:
  resources_evaluated: 15
  findings: 1
```

The Cloud Storage Client reports the container's public access level; the skill
interprets it as public exposure.

---

# Example 2 — Over-Permissive Role Assignment

## Request

```yaml
target: azure-subscription-00000000-0000-0000-0000-000000000000
assets:
  - asset-cloud-6102
subscription_scope_ref: azure-scope-example
credential_ref: azure-read-credential
scope_id: scope-example-2024
roe_id: roe-example-2024
options:
  check_roles: true
```

## Result

```yaml
findings:
  - id: finding-azure-5002
    title: Owner role assigned at subscription scope to an application principal
    weakness: CWE-732
    benchmark: CIS Azure Foundations - least privilege
    asset: asset-cloud-6102
    risk_ref: risk-azure-3002
    evidence_refs:
      - evidence-azure-7002
status: completed
metrics:
  resources_evaluated: 15
  findings: 1
```

The Azure Client reports the role assignment; the skill interprets the subscription-scoped
Owner grant as over-permissive.

---

# Example 3 — Unrestricted Network Security Group

## Request

```yaml
target: azure-subscription-00000000-0000-0000-0000-000000000000
assets:
  - asset-cloud-6103
subscription_scope_ref: azure-scope-example
credential_ref: azure-read-credential
scope_id: scope-example-2024
roe_id: roe-example-2024
options:
  check_network_exposure: true
```

## Result

```yaml
findings:
  - id: finding-azure-5003
    title: Network security group permits unrestricted ingress to management port
    weakness: CWE-284
    benchmark: CIS Azure Foundations - restrict management ports
    asset: asset-cloud-6103
    risk_ref: risk-azure-3003
    evidence_refs:
      - evidence-azure-7003
status: completed
metrics:
  resources_evaluated: 15
  findings: 1
```

The Azure Client reports the NSG rule; the skill interprets unrestricted ingress to a
management port as network exposure.

---

# Example 4 — Requires Approval

## Request

```yaml
target: azure-subscription-00000000-0000-0000-0000-000000000000
subscription_scope_ref: azure-scope-example
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings: []
status: awaiting_approval
metrics:
  approvals_requested: 1
```

The Rules of Engagement require approval before metadata collection; the skill defers
until approval is granted.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
