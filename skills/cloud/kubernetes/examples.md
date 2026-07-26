# Kubernetes Cloud Security Skill Examples

**File:** `skills/cloud/kubernetes/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Kubernetes Cloud
Security Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — Over-Permissive RBAC

## Request

```yaml
target: k8s-cluster-prod
assets:
  - asset-cloud-6301
namespace_scope_ref: k8s-scope-example
credential_ref: k8s-read-credential
scope_id: scope-example-2024
roe_id: roe-example-2024
options:
  check_rbac: true
```

## Result

```yaml
findings:
  - id: finding-k8s-5001
    title: cluster-admin bound to a namespace service account
    weakness: CWE-732
    benchmark: CIS Kubernetes - minimize cluster-admin use
    asset: asset-cloud-6301
    risk_ref: risk-k8s-3001
    evidence_refs:
      - evidence-k8s-7001
observations:
  - id: obs-k8s-4001
    kind: rbac-analysis
evidence:
  - id: evidence-k8s-7001
    observation_ref: obs-k8s-4001
status: completed
metrics:
  resources_evaluated: 40
  findings: 1
```

The Kubernetes Client reports the binding; the skill interprets the cluster-admin grant to
a namespace service account as over-permissive.

---

# Example 2 — Privileged Container

## Request

```yaml
target: k8s-cluster-prod
assets:
  - asset-cloud-6302
namespace_scope_ref: k8s-scope-example
credential_ref: k8s-read-credential
scope_id: scope-example-2024
roe_id: roe-example-2024
options:
  check_workloads: true
```

## Result

```yaml
findings:
  - id: finding-k8s-5002
    title: Workload runs a privileged container with host path mount
    weakness: CWE-250
    benchmark: CIS Kubernetes - minimize privileged containers
    asset: asset-cloud-6302
    risk_ref: risk-k8s-3002
    evidence_refs:
      - evidence-k8s-7002
status: completed
metrics:
  resources_evaluated: 40
  findings: 1
```

The Kubernetes Client reports the pod specification; the skill interprets the privileged
flag and hostPath mount as insecure workload settings.

---

# Example 3 — Secrets Exposed In Workload Environment

## Request

```yaml
target: k8s-cluster-prod
assets:
  - asset-cloud-6303
namespace_scope_ref: k8s-scope-example
credential_ref: k8s-read-credential
scope_id: scope-example-2024
roe_id: roe-example-2024
options:
  check_secrets: true
```

## Result

```yaml
findings:
  - id: finding-k8s-5003
    title: Secret value referenced in plaintext environment variable
    weakness: CWE-312
    benchmark: CIS Kubernetes - protect secret data
    asset: asset-cloud-6303
    risk_ref: risk-k8s-3003
    evidence_refs:
      - evidence-k8s-7003
status: completed
metrics:
  resources_evaluated: 40
  findings: 1
```

The Kubernetes Client reports the workload environment; the skill interprets the plaintext
secret reference as exposure. The secret value is redacted in evidence.

---

# Example 4 — Requires Approval

## Request

```yaml
target: k8s-cluster-prod
namespace_scope_ref: k8s-scope-example
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
