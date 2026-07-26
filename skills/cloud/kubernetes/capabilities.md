# Kubernetes Cloud Security Skill Capabilities

**File:** `skills/cloud/kubernetes/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Kubernetes Cloud Security Skill. Each
capability is scope-confined, policy-gated, evidence-backed, and tool independent.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| K8S-1 | RBAC posture analysis | kubernetes-client metadata | RBAC Findings |
| K8S-2 | Workload security analysis | kubernetes-client metadata | Workload Findings |
| K8S-3 | Exposure analysis | kubernetes-client metadata | Exposure Findings |
| K8S-4 | Network-policy analysis | kubernetes-client metadata | Network Findings |
| K8S-5 | Secret handling analysis | kubernetes-client metadata | Secret Findings |
| K8S-6 | Evidence recording | Observations | Evidence references |

---

# K8S-1 — RBAC Posture Analysis

The skill SHALL interpret observed roles, cluster roles, and bindings and identify
over-permissive authorization such as cluster-admin or wildcard verbs bound broadly.
Confirmed weaknesses SHALL be classified as CWE-732 or CWE-269 and referenced to the CIS
Kubernetes Benchmark RBAC controls.

---

# K8S-2 — Workload Security Analysis

The skill SHALL interpret workload specifications and identify insecure settings such as
privileged containers, host namespace sharing, and hostPath mounts. Confirmed weaknesses
SHALL be classified as CWE-250.

---

# K8S-3 — Exposure Analysis

The skill SHALL interpret API server, dashboard, and service configuration and identify
anonymous or unauthenticated access. Confirmed weaknesses SHALL be classified as CWE-306.

---

# K8S-4 — Network-Policy Analysis

The skill SHALL interpret network policy coverage and identify namespaces or workloads
lacking segmentation. Confirmed weaknesses SHALL be classified as CWE-284.

---

# K8S-5 — Secret Handling Analysis

The skill SHALL interpret workload specifications and identify secrets exposed in
environment variables or specifications. Confirmed weaknesses SHALL be classified as
CWE-312.

---

# K8S-6 — Evidence Recording

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
supporting ones to [Evidence](../../../schemas/evidence.md), redacting sensitive values.

---

# Capability Boundaries

The skill SHALL NOT

- Call the Kubernetes API directly
- Mutate the cluster or execute workloads
- Assess the container engine, TLS posture, or application-layer weaknesses
- Perform destructive exploitation

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface
operations in [interface.md](interface.md).
