# ADR-001 — Terraform Cloud Security Skill

**File:** `skills/cloud/terraform/adr/ADR-001-terraform-cloud-security-skill.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

The RPP platform assesses infrastructure-as-code for security posture weaknesses before
infrastructure is provisioned. Terraform configuration declares cloud resources, access
grants, and provider settings whose insecure declarations — public resources, missing
encryption, over-permissive access, and hardcoded secrets — can be identified statically.

Static analysis of declared configuration is distinct from assessing deployed resources.
The provider Cloud Security skills (AWS, Azure, GCP) interpret live provider metadata; the
Terraform skill interprets declared configuration read from the filesystem. The Filesystem
Client shared skill provides confined, bounded file access but performs no interpretation.

A dedicated domain skill is required to interpret declared Terraform configuration, classify
weaknesses, and emit evidence-backed findings, while never provisioning infrastructure,
never contacting providers, and never invoking tools.

---

# Decision

We SHALL provide a Terraform Cloud Security Skill in the Cloud Security tier with the
following properties.

- It reads declared configuration through the
  [Filesystem Client](../../../shared/filesystem-client/README.md) and SHALL NOT provision,
  plan, apply, or destroy infrastructure, nor contact provider APIs.
- It consults the [Policy Engine](../../../shared/policy-engine/README.md) before every
  target-facing action.
- It interprets declared resource, exposure, encryption, access, and secret posture and
  classifies weaknesses using CWE identifiers aligned to recognized infrastructure-as-code
  benchmarks.
- It produces and enriches `cloud-resource` [Assets](../../../../schemas/asset.md) and emits
  [Findings](../../../../schemas/finding.md) with [Risk](../../../../schemas/risk.md), each
  backed by [Evidence](../../../../schemas/evidence.md).
- It delegates deployed-resource assessment to the provider Cloud Security skills, TLS
  posture to TLS Analysis, and application weaknesses to Web Security skills.

---

# Consequences

## Positive

- Insecure configuration is detected before provisioning, shifting assessment left.
- Static interpretation is cleanly separated from the Filesystem Client that only reads
  files.
- Findings are evidence-backed and benchmark-aligned.

## Negative

- Static analysis cannot observe runtime state; deployed-resource assessment remains the
  province of the provider skills.

## Neutral

- Module and remote-source awareness and state-file posture are deferred to future
  extensions.

---

# Alternatives Considered

- Executing Terraform to produce a plan. Rejected because the skill is tool independent and
  SHALL NOT invoke tools or provision infrastructure.
- Folding IaC analysis into the provider skills. Rejected because static configuration
  analysis and live provider interpretation are distinct concerns with distinct inputs.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [Filesystem Client](../../../shared/filesystem-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
