# AWS Cloud Security Skill

**File:** `skills/cloud/aws/README.md`

**Version:** 1.0.0

---

# Purpose

The AWS Cloud Security Skill is a Cloud-Security-tier domain skill that evaluates the
security posture of an in-scope Amazon Web Services environment within the Robust
PenTest Platform (RPP).

It interprets provider-native AWS metadata — IAM, compute, networking, storage, and
instance-metadata configuration — into evidence-backed findings covering identity and
access weaknesses, public exposure, missing encryption, and insecure defaults.

The skill consumes provider-native metadata from the
[AWS Client](../../shared/aws-client/README.md) and object-storage exposure metadata
from the [Cloud Storage Client](../../shared/cloud-storage-client/README.md). It SHALL
NOT call AWS service APIs directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The AWS Cloud Security Skill SHALL

- Evaluate IAM identity and access posture from observed policies and permissions
- Evaluate public exposure of storage, compute, and network resources
- Evaluate encryption-at-rest and in-transit enforcement
- Evaluate insecure defaults such as legacy instance-metadata service configuration
- Consume `cloud-resource` [Assets](../../../schemas/asset.md) and enrich them
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with [Risk](../../../schemas/risk.md)
- Remain tool independent

---

# Non-Goals

The AWS Cloud Security Skill SHALL NOT

- Call AWS service APIs or perform provider I/O directly
- Enumerate provider resources itself beyond the shared client interface
- Assess general server-side TLS posture (that is TLS Analysis)
- Test application-layer weaknesses such as injection or XSS (those are Web Security
  skills)
- Assess Kubernetes clusters (that is the Kubernetes Cloud Security skill)
- Perform destructive or disruptive exploitation
- Invoke command-line tools or parse their output

Provider transport belongs to the shared AWS and Cloud Storage clients; cluster
assessment belongs to the Kubernetes skill; application weaknesses belong to Web
Security skills.

---

# Design Principles

The AWS Cloud Security Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same observed metadata
- Read-oriented — it interprets observed metadata and does not mutate the environment
- Provider-native — it reasons over AWS resource models
- Tool independent

---

# Architecture

```
Cloud Security Agent

↓

AWS Cloud Security Skill

├── Policy Gate               → Policy Engine
├── Metadata Collector        → AWS Client
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

The AWS Cloud Security Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Collecting provider-native metadata through the
  [AWS Client](../../shared/aws-client/README.md) and
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

Collect Provider-Native Metadata (AWS Client, Cloud Storage Client)

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

account_scope_ref:

credential_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope AWS environment. `assets` reference `cloud-resource`
[Assets](../../../schemas/asset.md). `account_scope_ref` references the authorized
accounts, regions, and services. `credential_ref` references authorized read
credentials by reference only. `scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill MAY produce and enrich `cloud-resource`
[Assets](../../../schemas/asset.md) representing AWS resources such as buckets, roles,
instances, and security groups. It SHALL NOT invent Asset types.

---

# Produced Findings

These weaknesses align with the CIS Amazon Web Services Foundations Benchmark and CWE.
The references are informational and do not change capability scope.

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- Publicly accessible storage bucket or object (CWE-284)
- Over-permissive IAM policy granting wildcard actions or resources (CWE-732)
- Security group permitting unrestricted ingress to sensitive ports (CWE-284)
- Legacy instance metadata service (IMDSv1) permitted, increasing SSRF exposure
  (CWE-16)
- Storage or volume without encryption at rest (CWE-311)
- Publicly shared machine image or snapshot (CWE-284)

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md) with
sensitive values redacted.

---

# Policy Enforcement

The AWS Cloud Security Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Metadata collection is a read action and SHALL proceed only on an `allow`
decision. Where a decision is `requires_approval`, the skill SHALL defer the action.
The skill SHALL NOT mutate the environment; any remediation or mutation is out of
scope. Out-of-scope accounts SHALL never be assessed.

---

# Dependencies

The AWS Cloud Security Skill depends on

- [AWS Client](../../shared/aws-client/README.md)
- [Cloud Storage Client](../../shared/cloud-storage-client/README.md)
- [Secrets Client](../../shared/secrets-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The AWS Cloud Security Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Cloud Security Agent and cloud workflows
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for AWS security weaknesses
- Enriched `cloud-resource` Assets
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The AWS Cloud Security Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Interpret observed metadata without mutating the environment
- Protect credentials and sensitive values from evidence and logs
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical identifiers and CIS Benchmark references
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `cloud-resource` Assets, an account scope, and read credentials
- Rely on the skill for AWS-specific interpretation
- Route TLS posture and application weaknesses to the dedicated skills
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Call AWS service APIs directly
- Bypass the Policy Engine
- Request environment mutation
- Assess out-of-scope accounts

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
- adr/ADR-001-aws-cloud-security-skill.md

---

# Related Packages

- [AWS Client](../../shared/aws-client/README.md)
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

- [ADR-001 — AWS Cloud Security Skill](adr/ADR-001-aws-cloud-security-skill.md)

---

# Future Extensions

Future versions MAY support

- Organization-wide posture aggregation
- Configuration-drift detection
- Additional service coverage
- Correlation with Discovery cloud inventory

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant AWS Cloud Security Skill produces evidence-backed Findings for AWS security
weaknesses by interpreting provider-native metadata, acting strictly within scope and
Rules of Engagement through the Policy Engine, without mutating the environment or
invoking tools directly.
