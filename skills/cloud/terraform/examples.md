# Terraform Cloud Security Skill Examples

**File:** `skills/cloud/terraform/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Terraform Cloud
Security Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — Declared Public Bucket

## Request

```yaml
target: terraform-config-app-infra
assets:
  - asset-repo-6501
configuration_root_ref: iac-root-example
scope_id: scope-example-2024
roe_id: roe-example-2024
options:
  check_public_exposure: true
```

## Result

```yaml
findings:
  - id: finding-tf-5001
    title: Declared storage bucket permits public access
    weakness: CWE-284
    benchmark: CIS Foundations Benchmark - restrict public storage access
    asset: asset-repo-6501
    risk_ref: risk-tf-3001
    evidence_refs:
      - evidence-tf-7001
observations:
  - id: obs-tf-4001
    kind: public-exposure-analysis
evidence:
  - id: evidence-tf-7001
    observation_ref: obs-tf-4001
status: completed
metrics:
  files_evaluated: 18
  resources_evaluated: 55
  findings: 1
```

The Filesystem Client provides the declared bucket configuration; the skill interprets the
public access setting as declared public exposure.

---

# Example 2 — Missing Encryption At Rest

## Request

```yaml
target: terraform-config-app-infra
assets:
  - asset-repo-6501
configuration_root_ref: iac-root-example
scope_id: scope-example-2024
roe_id: roe-example-2024
options:
  check_encryption: true
```

## Result

```yaml
findings:
  - id: finding-tf-5002
    title: Declared volume does not enable encryption at rest
    weakness: CWE-311
    benchmark: CIS Foundations Benchmark - encrypt data at rest
    asset: asset-repo-6501
    risk_ref: risk-tf-3002
    evidence_refs:
      - evidence-tf-7002
status: completed
metrics:
  files_evaluated: 18
  resources_evaluated: 55
  findings: 1
```

The declared volume omits encryption; the skill interprets the omission as missing
encryption at rest.

---

# Example 3 — Hardcoded Secret In Configuration

## Request

```yaml
target: terraform-config-app-infra
assets:
  - asset-repo-6501
configuration_root_ref: iac-root-example
scope_id: scope-example-2024
roe_id: roe-example-2024
options:
  check_secrets: true
```

## Result

```yaml
findings:
  - id: finding-tf-5003
    title: Hardcoded credential in configuration variable
    weakness: CWE-798
    benchmark: Secrets management guidance - no hardcoded credentials
    asset: asset-repo-6501
    risk_ref: risk-tf-3003
    evidence_refs:
      - evidence-tf-7003
status: completed
metrics:
  files_evaluated: 18
  resources_evaluated: 55
  findings: 1
```

The configuration declares a credential inline; the skill interprets it as a hardcoded
secret. The credential value is redacted in evidence.

---

# Example 4 — Requires Approval

## Request

```yaml
target: terraform-config-app-infra
configuration_root_ref: iac-root-example
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

The Rules of Engagement require approval before reading configuration; the skill defers
until approval is granted.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
