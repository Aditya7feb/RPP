# GCP Cloud Security Skill

**File:** `skills/cloud/gcp/README.md`

**Version:** 1.0.0

---

# Purpose

The GCP Cloud Security Skill is a Cloud-Security-tier domain skill that evaluates the
security posture of an in-scope Google Cloud Platform environment within the Robust
PenTest Platform (RPP).

It interprets provider-native GCP metadata — IAM policy bindings, compute, networking,
storage, and metadata-server configuration — into evidence-backed findings covering
identity and access weaknesses, public exposure, missing encryption, and insecure
defaults.

The skill consumes provider-native metadata from the
[GCP Client](../../shared/gcp-client/README.md) and object-storage exposure metadata from
the [Cloud Storage Client](../../shared/cloud-storage-client/README.md). It SHALL NOT call
GCP service APIs directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The GCP Cloud Security Skill SHALL

- Evaluate IAM binding and access posture from observed policies and permissions
- Evaluate public exposure of storage, compute, and network resources
- Evaluate encryption-at-rest and in-transit enforcement
- Evaluate insecure defaults such as default service accounts and metadata exposure
- Consume `cloud-resource` [Assets](../../../schemas/asset.md) and enrich them
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with [Risk](../../../schemas/risk.md)
- Remain tool independent

---

# Non-Goals

The GCP Cloud Security Skill SHALL NOT

- Call GCP service APIs or perform provider I/O directly
- Enumerate provider resources itself beyond the shared client interface
- Assess general server-side TLS posture (that is TLS Analysis)
- Test application-layer weaknesses such as injection or XSS (those are Web Security
  skills)
- Assess Kubernetes clusters (that is the Kubernetes Cloud Security skill)
- Perform destructive or disruptive exploitation
- Invoke command-line tools or parse their output

Provider transport belongs to the shared GCP and Cloud Storage clients; cluster assessment
belongs to the Kubernetes skill; application weaknesses belong to Web Security skills.

---

# Design Principles

The GCP Cloud Security Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same observed metadata
- Read-oriented — it interprets observed metadata and does not mutate the environment
- Provider-native — it reasons over GCP resource models
- Tool independent

---

# Architecture

```
Cloud Security Agent

↓

GCP Cloud Security Skill

├── Policy Gate               → Policy Engine
├── Metadata Collector        → GCP Client
├── Storage Exposure Collector → Cloud Storage Client
├── IAM Analyzer
├── Exposure Analyzer
├── Encryption Analyzer
├── Insecure-Default Analyzer
├── Weakness Analyzer
├── Evidence Recorder         → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill interprets provider-native metadata and SHALL remain unaware of any provider
API implementation.

---

# Responsibilities

The GCP Cloud Security Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Collecting provider-native metadata through the
  [GCP Client](../../shared/gcp-client/README.md) and
  [Cloud Storage Client](../../shared/cloud-storage-client/README.md)
- Analyzing IAM, exposure, encryption, and insecure-default posture
- Recording [Observations](../../../schemas/observation.md) and
  [Evidence](../../../schemas/evidence.md)
- Emitting [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md)

---

# Assessment Lifecycle

```
Receive Environment Target And Scope

↓

Consult Policy Engine (per action)

↓

Collect Provider-Native Metadata (GCP Client, Cloud Storage Client)

↓

Analyze IAM, Exposure, Encryption, And Insecure Defaults

↓

Record Observations → Evidence

↓

Analyze For Cloud Security Weaknesses

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

project_scope_ref:

credential_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope GCP environment. `assets` reference `cloud-resource`
[Assets](../../../schemas/asset.md). `project_scope_ref` references authorized
organizations, projects, regions, and services. `credential_ref` references authorized
read credentials by reference only. `scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill MAY produce and enrich `cloud-resource`
[Assets](../../../schemas/asset.md) representing GCP resources such as buckets, IAM
bindings, instances, and firewall rules. It SHALL NOT invent Asset types.

---

# Produced Findings

These weaknesses align with the CIS Google Cloud Platform Foundations Benchmark and CWE.
The references are informational and do not change capability scope.

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- Publicly accessible storage bucket or object, including `allUsers` bindings (CWE-284)
- Over-permissive IAM binding granting primitive roles such as Owner or Editor (CWE-732)
- Firewall rule permitting unrestricted ingress to sensitive ports (CWE-284)
- Default service account with broad scopes, or exposed metadata server (CWE-16)
- Storage or disk without customer-managed or default encryption assurances (CWE-311)

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md) with
sensitive values redacted.

---

# Policy Enforcement

The GCP Cloud Security Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing action.
Metadata collection is a read action and SHALL proceed only on an `allow` decision. Where
a decision is `requires_approval`, the skill SHALL defer the action. The skill SHALL NOT
mutate the environment. Out-of-scope projects SHALL never be assessed.

---

# Dependencies

The GCP Cloud Security Skill depends on

- [GCP Client](../../shared/gcp-client/README.md)
- [Cloud Storage Client](../../shared/cloud-storage-client/README.md)
- [Secrets Client](../../shared/secrets-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The GCP Cloud Security Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Cloud Security Agent and cloud workflows
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for GCP security weaknesses
- Enriched `cloud-resource` Assets
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The GCP Cloud Security Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Interpret observed metadata without mutating the environment
- Protect credentials and sensitive values from evidence and logs
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical identifiers and CIS Benchmark references
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `cloud-resource` Assets, a project scope, and read credentials
- Rely on the skill for GCP-specific interpretation
- Route TLS posture and application weaknesses to the dedicated skills
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Call GCP service APIs directly
- Bypass the Policy Engine
- Request environment mutation
- Assess out-of-scope projects

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
- adr/ADR-001-gcp-cloud-security-skill.md

---

# Related Packages

- [GCP Client](../../shared/gcp-client/README.md)
- [Cloud Storage Client](../../shared/cloud-storage-client/README.md)
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

- [ADR-001 — GCP Cloud Security Skill](adr/ADR-001-gcp-cloud-security-skill.md)

---

# Future Extensions

Future versions MAY support

- Organization-policy posture aggregation
- Configuration-drift detection
- Additional service coverage
- Correlation with Discovery cloud inventory

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant GCP Cloud Security Skill produces evidence-backed Findings for GCP security
weaknesses by interpreting provider-native metadata, acting strictly within scope and
Rules of Engagement through the Policy Engine, without mutating the environment or invoking
tools directly.
