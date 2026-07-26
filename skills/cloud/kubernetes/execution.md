# Kubernetes Cloud Security Skill Execution

**File:** `skills/cloud/kubernetes/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Kubernetes Cloud Security
Skill, stage by stage. Given the same observed metadata and configuration, execution SHALL
be reproducible.

---

# Execution Stages

```
Stage 1  Intake And Scope Validation
Stage 2  Policy Consultation
Stage 3  Metadata Collection
Stage 4  RBAC Posture Analysis
Stage 5  Workload Security Analysis
Stage 6  Exposure Analysis
Stage 7  Network And Secret Analysis
Stage 8  Weakness Analysis And Finding Emission
```

---

# Stage 1 — Intake And Scope Validation

The skill SHALL validate that the target and referenced Assets are within
[Scope](../../../schemas/scope.md). Out-of-scope namespaces SHALL be rejected before any
action.

---

# Stage 2 — Policy Consultation

Before every target-facing action, the skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md). Only an `allow` decision permits the
action. A `requires_approval` decision SHALL defer the action.

---

# Stage 3 — Metadata Collection

The skill SHALL collect provider-native metadata through the
[Kubernetes Client](../../shared/kubernetes-client/README.md). Collection is read-only,
uses get, list, and access-review requests, and is bounded by configured limits.

---

# Stage 4 — RBAC Posture Analysis

The skill SHALL interpret roles, cluster roles, and bindings and record over-permissive
authorization as Observations classified CWE-732 or CWE-269.

---

# Stage 5 — Workload Security Analysis

The skill SHALL interpret workload specifications and record insecure settings such as
privileged containers, host namespaces, and hostPath mounts as Observations classified
CWE-250.

---

# Stage 6 — Exposure Analysis

The skill SHALL interpret API server, dashboard, and service configuration and record
anonymous or unauthenticated access as Observations classified CWE-306.

---

# Stage 7 — Network And Secret Analysis

The skill SHALL interpret network policy coverage and workload secret handling and record
missing segmentation as Observations classified CWE-284 and exposed secrets as Observations
classified CWE-312.

---

# Stage 8 — Weakness Analysis And Finding Emission

The skill SHALL analyze recorded Observations, promote supporting ones to
[Evidence](../../../schemas/evidence.md), and emit
[Findings](../../../schemas/finding.md) with [Risk](../../../schemas/risk.md). Every
Finding SHALL reference supporting Evidence.

---

# Determinism

Given identical observed metadata, Assets, and configuration, the skill SHALL produce
identical Findings.

---

# Idempotence

Assessment SHALL NOT alter the cluster or execute workloads. Repeated assessment SHALL NOT
accumulate side effects.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
