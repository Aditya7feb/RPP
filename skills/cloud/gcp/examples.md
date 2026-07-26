# GCP Cloud Security Skill Examples

**File:** `skills/cloud/gcp/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the GCP Cloud Security
Skill. Examples illustrate the interface and outputs; they contain no implementation code.

---

# Example 1 — Publicly Accessible Storage Bucket

## Request

```yaml
target: gcp-project-app-prod
assets:
  - asset-cloud-6201
project_scope_ref: gcp-scope-example
credential_ref: gcp-read-credential
scope_id: scope-example-2024
roe_id: roe-example-2024
options:
  check_public_exposure: true
```

## Result

```yaml
findings:
  - id: finding-gcp-5001
    title: Storage bucket grants access to allUsers
    weakness: CWE-284
    benchmark: CIS GCP Foundations - storage public access
    asset: asset-cloud-6201
    risk_ref: risk-gcp-3001
    evidence_refs:
      - evidence-gcp-7001
observations:
  - id: obs-gcp-4001
    kind: public-exposure-analysis
evidence:
  - id: evidence-gcp-7001
    observation_ref: obs-gcp-4001
status: completed
metrics:
  resources_evaluated: 14
  findings: 1
```

The Cloud Storage Client reports an `allUsers` binding on the bucket; the skill interprets
it as public exposure.

---

# Example 2 — Over-Permissive IAM Binding

## Request

```yaml
target: gcp-project-app-prod
assets:
  - asset-cloud-6202
project_scope_ref: gcp-scope-example
credential_ref: gcp-read-credential
scope_id: scope-example-2024
roe_id: roe-example-2024
options:
  check_iam: true
```

## Result

```yaml
findings:
  - id: finding-gcp-5002
    title: Primitive Owner role bound to a service account
    weakness: CWE-732
    benchmark: CIS GCP Foundations - avoid primitive roles
    asset: asset-cloud-6202
    risk_ref: risk-gcp-3002
    evidence_refs:
      - evidence-gcp-7002
status: completed
metrics:
  resources_evaluated: 14
  findings: 1
```

The GCP Client reports the project IAM policy; the skill interprets the primitive Owner
binding as over-permissive.

---

# Example 3 — Default Service Account With Broad Scopes

## Request

```yaml
target: gcp-project-app-prod
assets:
  - asset-cloud-6203
project_scope_ref: gcp-scope-example
credential_ref: gcp-read-credential
scope_id: scope-example-2024
roe_id: roe-example-2024
options:
  check_insecure_defaults: true
```

## Result

```yaml
findings:
  - id: finding-gcp-5003
    title: Instance uses default service account with broad scopes
    weakness: CWE-276
    benchmark: CIS GCP Foundations - restrict default service accounts
    asset: asset-cloud-6203
    risk_ref: risk-gcp-3003
    evidence_refs:
      - evidence-gcp-7003
status: completed
metrics:
  resources_evaluated: 14
  findings: 1
```

The GCP Client reports the instance service-account configuration; the skill interprets the
default account with broad scopes as an insecure default.

---

# Example 4 — Requires Approval

## Request

```yaml
target: gcp-project-app-prod
project_scope_ref: gcp-scope-example
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

The Rules of Engagement require approval before metadata collection; the skill defers until
approval is granted.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
