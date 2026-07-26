# Terraform Cloud Security Skill Capabilities

**File:** `skills/cloud/terraform/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Terraform Cloud Security Skill. Each
capability is scope-confined, policy-gated, evidence-backed, and tool independent.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| TF-1 | Resource configuration analysis | filesystem-client (IaC) | Configuration Findings |
| TF-2 | Public exposure analysis | filesystem-client (IaC) | Exposure Findings |
| TF-3 | Encryption analysis | filesystem-client (IaC) | Encryption Findings |
| TF-4 | Access grant analysis | filesystem-client (IaC) | Access Findings |
| TF-5 | Hardcoded secret analysis | filesystem-client (IaC) | Secret Findings |
| TF-6 | Evidence recording | Observations | Evidence references |

---

# TF-1 — Resource Configuration Analysis

The skill SHALL interpret declared resource configuration and identify insecure settings
such as missing logging or auditing. Confirmed weaknesses SHALL be classified as CWE-778 or
CWE-16 and referenced to recognized infrastructure-as-code benchmarks.

---

# TF-2 — Public Exposure Analysis

The skill SHALL interpret declared resource configuration and identify public exposure such
as a public bucket or unrestricted ingress rule. Confirmed weaknesses SHALL be classified as
CWE-284.

---

# TF-3 — Encryption Analysis

The skill SHALL interpret declared resource configuration and identify missing encryption at
rest. Confirmed weaknesses SHALL be classified as CWE-311.

---

# TF-4 — Access Grant Analysis

The skill SHALL interpret declared access grants and identify over-permissive grants such as
wildcard actions or resources. Confirmed weaknesses SHALL be classified as CWE-732.

---

# TF-5 — Hardcoded Secret Analysis

The skill SHALL interpret configuration and variables and identify hardcoded secrets or
credentials. Confirmed weaknesses SHALL be classified as CWE-798.

---

# TF-6 — Evidence Recording

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
supporting ones to [Evidence](../../../schemas/evidence.md), redacting sensitive values.

---

# Capability Boundaries

The skill SHALL NOT

- Provision, plan, or apply infrastructure
- Contact cloud provider APIs
- Execute Terraform or any tool
- Assess deployed resources, TLS posture, or application-layer weaknesses

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface
operations in [interface.md](interface.md).
