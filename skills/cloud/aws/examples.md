# AWS Cloud Security Skill Examples

**File:** `skills/cloud/aws/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the AWS Cloud Security
Skill. Examples illustrate the interface and outputs; they contain no implementation
code.

---

# Example 1 — Publicly Accessible Storage Bucket

## Request

```yaml
target: aws-account-111122223333
assets:
  - asset-cloud-6001
account_scope_ref: aws-scope-example
credential_ref: aws-read-credential
scope_id: scope-example-2024
roe_id: roe-example-2024
options:
  check_public_exposure: true
```

## Result

```yaml
findings:
  - id: finding-aws-5001
    title: Storage bucket is publicly accessible
    weakness: CWE-284
    benchmark: CIS AWS Foundations - storage public access
    asset: asset-cloud-6001
    risk_ref: risk-aws-3001
    evidence_refs:
      - evidence-aws-7001
observations:
  - id: obs-aws-4001
    kind: public-exposure-analysis
evidence:
  - id: evidence-aws-7001
    observation_ref: obs-aws-4001
status: completed
metrics:
  resources_evaluated: 12
  findings: 1
```

The Cloud Storage Client reports the bucket's public access metadata; the skill
interprets it as public exposure.

---

# Example 2 — Over-Permissive IAM Policy

## Request

```yaml
target: aws-account-111122223333
assets:
  - asset-cloud-6002
account_scope_ref: aws-scope-example
credential_ref: aws-read-credential
scope_id: scope-example-2024
roe_id: roe-example-2024
options:
  check_iam: true
```

## Result

```yaml
findings:
  - id: finding-aws-5002
    title: IAM policy grants wildcard actions on all resources
    weakness: CWE-732
    benchmark: CIS AWS Foundations - least privilege
    asset: asset-cloud-6002
    risk_ref: risk-aws-3002
    evidence_refs:
      - evidence-aws-7002
status: completed
metrics:
  resources_evaluated: 12
  findings: 1
```

The AWS Client reports the attached policy document; the skill interprets the wildcard
grant as over-permissive.

---

# Example 3 — Legacy Instance Metadata Service Permitted

## Request

```yaml
target: aws-account-111122223333
assets:
  - asset-cloud-6003
account_scope_ref: aws-scope-example
credential_ref: aws-read-credential
scope_id: scope-example-2024
roe_id: roe-example-2024
options:
  check_insecure_defaults: true
```

## Result

```yaml
findings:
  - id: finding-aws-5003
    title: Instance permits legacy metadata service (IMDSv1)
    weakness: CWE-1188
    benchmark: CIS AWS Foundations - IMDSv2 required
    asset: asset-cloud-6003
    risk_ref: risk-aws-3003
    evidence_refs:
      - evidence-aws-7003
status: completed
metrics:
  resources_evaluated: 12
  findings: 1
```

The AWS Client reports the instance metadata options; the skill interprets IMDSv1
availability as an insecure default that increases SSRF exposure.

---

# Example 4 — Requires Approval

## Request

```yaml
target: aws-account-111122223333
account_scope_ref: aws-scope-example
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
