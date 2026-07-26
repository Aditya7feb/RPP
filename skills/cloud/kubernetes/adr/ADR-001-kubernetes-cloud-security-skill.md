# ADR-001 — Kubernetes Cloud Security Skill

**File:** `skills/cloud/kubernetes/adr/ADR-001-kubernetes-cloud-security-skill.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

The RPP platform assesses Kubernetes clusters for security posture weaknesses spanning
authorization (RBAC), workload security, exposure, network segmentation, and secret
handling. These concerns require interpreting provider-native Kubernetes metadata — roles,
bindings, workload specifications, network policies, and service configuration — against
recognized benchmarks.

The Kubernetes Client shared skill provides confined, read-preferring access to
provider-native cluster metadata but deliberately performs no interpretation and produces
no findings. A dedicated domain skill is required to interpret that metadata, classify
weaknesses, and emit evidence-backed findings, while never calling the Kubernetes API
directly, never mutating the cluster or executing workloads, and delegating container-engine
assessment, TLS posture, and application-layer weaknesses to their respective tiers.

The MASTER_PLAN groups Helm, Istio, and Ingress under this Cloud Security phase; these are
Kubernetes-ecosystem concerns whose resources are assessed as Kubernetes workloads and
configuration through this skill rather than as separate skills.

---

# Decision

We SHALL provide a Kubernetes Cloud Security Skill in the Cloud Security tier with the
following properties.

- It consumes provider-native metadata through the
  [Kubernetes Client](../../../shared/kubernetes-client/README.md) and SHALL NOT call the
  Kubernetes API directly.
- It consults the [Policy Engine](../../../shared/policy-engine/README.md) before every
  target-facing action.
- It interprets RBAC, workload, exposure, network-policy, and secret posture and classifies
  weaknesses using CWE identifiers aligned to the CIS Kubernetes Benchmark.
- It evaluates Helm-, Istio-, and Ingress-managed resources as Kubernetes workloads and
  configuration.
- It produces and enriches `cloud-resource` [Assets](../../../../schemas/asset.md) and emits
  [Findings](../../../../schemas/finding.md) with [Risk](../../../../schemas/risk.md), each
  backed by [Evidence](../../../../schemas/evidence.md).
- It does not mutate the cluster or execute workloads and delegates container-engine
  assessment to the Docker skill, TLS posture to TLS Analysis, and application weaknesses to
  Web Security skills.

---

# Consequences

## Positive

- Cluster posture interpretation is centralized in a cohesive, tool-independent skill.
- Interpretation is cleanly separated from the shared client that only reports metadata.
- Helm, Istio, and Ingress resources are covered without separate skills.
- Findings are evidence-backed and benchmark-aligned.

## Negative

- The skill depends on the breadth of metadata the shared client exposes.

## Neutral

- Admission-controller posture and pod security standard conformance are deferred to future
  extensions.

---

# Alternatives Considered

- Interpreting cluster posture inside the Kubernetes Client. Rejected because the shared
  client reports metadata as data and must not embed security interpretation.
- Separate Helm, Istio, and Ingress skills. Rejected because their resources are Kubernetes
  workloads and configuration best assessed through this skill.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [Kubernetes Client](../../../shared/kubernetes-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
