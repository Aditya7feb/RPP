# Terraform Cloud Security Skill

**File:** `skills/cloud/terraform/README.md`

**Version:** 1.0.0

---

# Purpose

The Terraform Cloud Security Skill is a Cloud-Security-tier domain skill that evaluates the
security posture of in-scope Terraform infrastructure-as-code (IaC) within the Robust
PenTest Platform (RPP).

It interprets declared Terraform configuration — resource definitions, variables, and
provider settings — into evidence-backed findings covering insecure declared configuration,
public exposure, missing encryption, over-permissive access, and hardcoded secrets, before
infrastructure is provisioned.

The skill reads IaC files through the
[Filesystem Client](../../shared/filesystem-client/README.md). It SHALL NOT provision,
plan, or apply infrastructure and SHALL NOT contact any cloud provider. Every target-facing
action is authorized by the [Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The Terraform Cloud Security Skill SHALL

- Evaluate declared resource configuration for insecure settings
- Evaluate declared public exposure of storage, compute, and network resources
- Evaluate declared encryption enforcement
- Evaluate declared access grants for over-permissiveness
- Evaluate configuration for hardcoded secrets
- Consume `repository` and `cloud-resource` [Assets](../../../schemas/asset.md) and enrich
  them
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with [Risk](../../../schemas/risk.md)
- Remain tool independent

---

# Non-Goals

The Terraform Cloud Security Skill SHALL NOT

- Provision, plan, apply, or destroy infrastructure
- Contact cloud provider APIs or perform provider I/O
- Execute Terraform or any command-line tool, or parse tool output
- Assess deployed cloud resources (those are the provider Cloud Security skills)
- Assess general server-side TLS posture (that is TLS Analysis)
- Test application-layer weaknesses such as injection or XSS (those are Web Security
  skills)

File access belongs to the shared Filesystem Client; deployed-resource assessment belongs
to the provider Cloud Security skills; application weaknesses belong to Web Security skills.

---

# Design Principles

The Terraform Cloud Security Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same configuration files
- Static — it interprets declared configuration and provisions nothing
- Provider-aware — it reasons over declared provider resource models
- Tool independent

---

# Architecture

```
Cloud Security Agent

↓

Terraform Cloud Security Skill

├── Policy Gate            → Policy Engine
├── Configuration Reader   → Filesystem Client
├── Resource Config Analyzer
├── Exposure Analyzer
├── Encryption Analyzer
├── Access Analyzer
├── Secret Analyzer
├── Weakness Analyzer
├── Evidence Recorder      → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill interprets declared configuration and SHALL remain unaware of any provisioning
implementation.

---

# Responsibilities

The Terraform Cloud Security Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Reading declared configuration through the
  [Filesystem Client](../../shared/filesystem-client/README.md)
- Analyzing declared resource, exposure, encryption, access, and secret posture
- Recording [Observations](../../../schemas/observation.md) and
  [Evidence](../../../schemas/evidence.md)
- Emitting [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md)

---

# Assessment Lifecycle

```
Receive Configuration Location And Scope

↓

Consult Policy Engine (per action)

↓

Read Declared Configuration (Filesystem Client)

↓

Analyze Resource Config, Exposure, Encryption, Access, And Secrets

↓

Record Observations → Evidence

↓

Analyze For Insecure Declared Configuration

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

configuration_root_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope Terraform configuration source. `assets` reference
`repository` or `cloud-resource` [Assets](../../../schemas/asset.md).
`configuration_root_ref` references the authorized filesystem root containing the
configuration. `scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill MAY produce and enrich `cloud-resource`
[Assets](../../../schemas/asset.md) representing resources declared in configuration. It
SHALL NOT invent Asset types.

---

# Produced Findings

These weaknesses align with recognized infrastructure-as-code and cloud security benchmarks
and CWE. The references are informational and do not change capability scope.

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- Declared resource with public access such as a public bucket or open ingress (CWE-284)
- Declared resource without encryption at rest (CWE-311)
- Declared access grant that is over-permissive such as wildcard actions (CWE-732)
- Hardcoded secret or credential in configuration or variables (CWE-798)
- Declared resource missing required logging or auditing (CWE-778)

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md) with
sensitive values redacted.

---

# Policy Enforcement

The Terraform Cloud Security Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing action.
Reading configuration is a read action and SHALL proceed only on an `allow` decision. Where
a decision is `requires_approval`, the skill SHALL defer the action. The skill SHALL NOT
provision, plan, or apply infrastructure. Out-of-scope configuration roots SHALL never be
read.

---

# Dependencies

The Terraform Cloud Security Skill depends on

- [Filesystem Client](../../shared/filesystem-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Terraform Cloud Security Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Cloud Security Agent and cloud workflows
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for insecure declared configuration
- Enriched `cloud-resource` Assets
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Terraform Cloud Security Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Interpret declared configuration without provisioning or contacting providers
- Protect secrets and sensitive values from evidence and logs
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical identifiers and benchmark references
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide an in-scope configuration root and relevant Assets
- Rely on the skill for declared-configuration interpretation
- Route deployed-resource, TLS, and application weaknesses to the dedicated skills
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Request provisioning, planning, or application of infrastructure
- Bypass the Policy Engine
- Provide out-of-scope configuration roots
- Expect deployed-resource assessment from this skill

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
- adr/ADR-001-terraform-cloud-security-skill.md

---

# Related Packages

- [Filesystem Client](../../shared/filesystem-client/README.md)
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

- [ADR-001 — Terraform Cloud Security Skill](adr/ADR-001-terraform-cloud-security-skill.md)

---

# Future Extensions

Future versions MAY support

- Module and remote-source awareness
- State-file posture evaluation where authorized
- Policy-as-code conformance
- Correlation with deployed-resource findings

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Terraform Cloud Security Skill produces evidence-backed Findings for insecure
declared configuration by statically interpreting infrastructure-as-code, acting strictly
within scope and Rules of Engagement through the Policy Engine, without provisioning
infrastructure, contacting providers, or invoking tools directly.
