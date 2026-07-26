# Kubernetes Cloud Security Skill

**File:** `skills/cloud/kubernetes/README.md`

**Version:** 1.0.0

---

# Purpose

The Kubernetes Cloud Security Skill is a Cloud-Security-tier domain skill that evaluates
the security posture of an in-scope Kubernetes cluster within the Robust PenTest Platform
(RPP).

It interprets provider-native Kubernetes metadata — RBAC, workload specifications,
network policies, and cluster configuration — into evidence-backed findings covering
authorization weaknesses, insecure workloads, exposure, and insecure defaults.

The skill consumes provider-native metadata from the
[Kubernetes Client](../../shared/kubernetes-client/README.md). It SHALL NOT call the
Kubernetes API directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The Kubernetes Cloud Security Skill SHALL

- Evaluate RBAC authorization posture from observed roles and bindings
- Evaluate workload security such as privileged containers and host access
- Evaluate exposure such as anonymous API access and exposed dashboards
- Evaluate network segmentation such as missing network policies
- Evaluate secret handling in workload specifications
- Consume `cloud-resource` [Assets](../../../schemas/asset.md) and enrich them
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with [Risk](../../../schemas/risk.md)
- Remain tool independent

---

# Non-Goals

The Kubernetes Cloud Security Skill SHALL NOT

- Call the Kubernetes API or perform cluster I/O directly
- Enumerate cluster resources itself beyond the shared client interface
- Assess the underlying container engine (that is the Docker Cloud Security skill)
- Assess general server-side TLS posture (that is TLS Analysis)
- Test application-layer weaknesses such as injection or XSS (those are Web Security
  skills)
- Perform destructive or disruptive exploitation such as workload execution
- Invoke command-line tools or parse their output

Cluster transport belongs to the shared Kubernetes Client; container-engine assessment
belongs to the Docker skill; application weaknesses belong to Web Security skills.

---

# Design Principles

The Kubernetes Cloud Security Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same observed metadata
- Read-oriented — it interprets observed metadata and does not mutate the cluster
- Provider-native — it reasons over Kubernetes resource models
- Tool independent

---

# Architecture

```
Cloud Security Agent

↓

Kubernetes Cloud Security Skill

├── Policy Gate           → Policy Engine
├── Metadata Collector    → Kubernetes Client
├── RBAC Analyzer
├── Workload Analyzer
├── Exposure Analyzer
├── Network-Policy Analyzer
├── Secret Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill interprets provider-native metadata and SHALL remain unaware of any API
implementation.

---

# Responsibilities

The Kubernetes Cloud Security Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Collecting provider-native metadata through the
  [Kubernetes Client](../../shared/kubernetes-client/README.md)
- Analyzing RBAC, workload, exposure, network, and secret posture
- Recording [Observations](../../../schemas/observation.md) and
  [Evidence](../../../schemas/evidence.md)
- Emitting [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md)

---

# Assessment Lifecycle

```
Receive Cluster Target And Scope

↓

Consult Policy Engine (per action)

↓

Collect Provider-Native Metadata (Kubernetes Client)

↓

Analyze RBAC, Workloads, Exposure, Network, And Secrets

↓

Record Observations → Evidence

↓

Analyze For Cluster Security Weaknesses

↓

Emit Findings and Risk (where applicable)
```

Every produced Finding SHALL be traceable to evidence.

---

# Inputs

The skill accepts

```yaml
target:

assets:

namespace_scope_ref:

credential_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope Kubernetes cluster. `assets` reference `cloud-resource`
[Assets](../../../schemas/asset.md). `namespace_scope_ref` references authorized
namespaces and resource kinds. `credential_ref` references authorized read credentials by
reference only. `scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill MAY produce and enrich `cloud-resource`
[Assets](../../../schemas/asset.md) representing Kubernetes resources such as roles,
bindings, workloads, and services. It SHALL NOT invent Asset types.

---

# Produced Findings

These weaknesses align with the CIS Kubernetes Benchmark and CWE. The references are
informational and do not change capability scope.

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- Over-permissive RBAC such as cluster-admin or wildcard verbs bound broadly (CWE-732)
- Privileged container or host namespace or hostPath access (CWE-250)
- Anonymous or unauthenticated API or dashboard access (CWE-306)
- Missing network policy permitting unrestricted pod-to-pod traffic (CWE-284)
- Secrets exposed in workload environment or specification (CWE-312)

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md) with
sensitive values redacted.

---

# Policy Enforcement

The Kubernetes Cloud Security Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing action.
Metadata collection is a read action and SHALL proceed only on an `allow` decision. Where
a decision is `requires_approval`, the skill SHALL defer the action. The skill SHALL NOT
mutate the cluster or execute workloads. Out-of-scope namespaces SHALL never be assessed.

---

# Dependencies

The Kubernetes Cloud Security Skill depends on

- [Kubernetes Client](../../shared/kubernetes-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Kubernetes Cloud Security Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Cloud Security Agent and cloud workflows
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for Kubernetes security weaknesses
- Enriched `cloud-resource` Assets
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Kubernetes Cloud Security Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Interpret observed metadata without mutating the cluster or executing workloads
- Protect credentials and sensitive values from evidence and logs
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical identifiers and CIS Benchmark references
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `cloud-resource` Assets, a namespace scope, and read credentials
- Rely on the skill for Kubernetes-specific interpretation
- Route container-engine, TLS, and application weaknesses to the dedicated skills
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Call the Kubernetes API directly
- Bypass the Policy Engine
- Request cluster mutation or workload execution
- Assess out-of-scope namespaces

---

# Documentation Requirements

This skill includes

- README.md
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md
- adr/ADR-001-kubernetes-cloud-security-skill.md

---

# Related Packages

- [Kubernetes Client](../../shared/kubernetes-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — Kubernetes Cloud Security Skill](adr/ADR-001-kubernetes-cloud-security-skill.md)

---

# Future Extensions

Future versions MAY support

- Admission-controller posture evaluation
- Pod security standard conformance
- Multi-cluster posture aggregation
- Correlation with Discovery cloud inventory

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Kubernetes Cloud Security Skill produces evidence-backed Findings for cluster
security weaknesses by interpreting provider-native metadata, acting strictly within scope
and Rules of Engagement through the Policy Engine, without mutating the cluster, executing
workloads, or invoking tools directly.
