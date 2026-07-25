# Kubernetes Client Examples

**File:** `skills/shared/kubernetes-client/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
Kubernetes Client Shared Skill in use.

Examples demonstrate scoped reads, RBAC observation, scope rejection, mutation
gating, forbidden mapping, evidence, and expected outputs.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Scoped List

A Kubernetes assessment skill lists pods within an authorized namespace.

## Invocation

```yaml
metadata:
  request_id: req-10201
  assessment_id: asmt-42
  task_id: task-k8s-audit
  skill_id: kubernetes-assessment
cluster_id: target-cluster
credential_ref: cred-k8s-audit
namespace: app
group: ""
version: v1
kind: pods
verb: list
options:
  max_items: 2000
```

## Result

```yaml
outcome: completed
items:
  - name: web-7d9f
    node: node-2
  - name: api-55c1
    node: node-3
```

The list is confined to the `app` namespace and bounded by `max_items`.

---

# Example 2 — RBAC Observation

The skill observes effective permissions as data.

## Result

```yaml
outcome: completed
rbac:
  can_list_secrets: true
  can_create_pods: false
  scope: namespace/app
```

Effective permissions are reported as data; whether they are over-permissive is
determined by domain skills.

---

# Example 3 — Scope Rejection

A resource outside the authorized scope is rejected.

## Invocation

```yaml
namespace: kube-system
kind: secrets
verb: list
```

## Result

```yaml
outcome: scope_rejected
error:
  category: Scope
  code: scope_rejected
  namespace: kube-system
  retryable: false
```

The confinement boundary prevents access outside authorized namespaces.

---

# Example 4 — Mutation Blocked

A create is attempted while mutations are disabled.

## Configuration

```yaml
execution:
  allow_mutations: false
```

## Result

```yaml
outcome: rejected
error:
  category: Governance
  code: mutation_blocked
  retryable: false
```

Mutations are intrusive and require authorization.

---

# Example 5 — Exec Requires Elevated Authorization

An exec into a pod is attempted while exec is disabled.

## Result

```yaml
outcome: rejected
error:
  category: Governance
  code: exec_blocked
  retryable: false
```

Workload execution requires explicit elevated authorization.

---

# Example 6 — Forbidden Mapped From API

The API server denies a permitted-scope request with `403`.

## Result

```yaml
outcome: forbidden
error:
  category: Authorization
  code: forbidden
  reason: "pods is forbidden: User cannot list resource"
  retryable: false
```

The API reason is preserved as data for domain interpretation.

---

# Example 7 — Evidence Record

A single operation produces the following evidence.

```yaml
evidence:
  type: kubernetes-operation
  cluster_id: target-cluster
  namespace: app
  kind: pods
  verb: list
  item_count: 2
  decided_at: 2026-07-25T18:30:00Z
```

The evidence conforms to the canonical
[Evidence schema](../../../schemas/evidence.md), excludes tokens and sensitive
contents, and supports auditing.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [HTTP Client](../http-client/README.md)
- [Secrets Client](../secrets-client/README.md)
