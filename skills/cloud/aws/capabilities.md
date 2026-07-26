# AWS Cloud Security Skill Capabilities

**File:** `skills/cloud/aws/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the AWS Cloud Security Skill. Each
capability is scope-confined, policy-gated, evidence-backed, and tool independent.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| AWS-1 | IAM posture analysis | aws-client metadata | IAM Findings |
| AWS-2 | Public exposure analysis | aws-client + cloud-storage-client | Exposure Findings |
| AWS-3 | Network exposure analysis | aws-client metadata | Network Findings |
| AWS-4 | Encryption analysis | aws-client metadata | Encryption Findings |
| AWS-5 | Insecure-default analysis | aws-client metadata | Configuration Findings |
| AWS-6 | Evidence recording | Observations | Evidence references |

---

# AWS-1 — IAM Posture Analysis

The skill SHALL interpret observed IAM principals, policies, and effective permissions
and identify over-permissive grants such as wildcard actions or resources. Confirmed
weaknesses SHALL be classified as CWE-732 or CWE-269 and referenced to the CIS AWS
Foundations Benchmark identity controls.

---

# AWS-2 — Public Exposure Analysis

The skill SHALL interpret storage access metadata from the
[Cloud Storage Client](../../shared/cloud-storage-client/README.md) and resource
sharing metadata from the [AWS Client](../../shared/aws-client/README.md) and identify
public exposure of buckets, objects, images, and snapshots. Confirmed exposure SHALL be
classified as CWE-284.

---

# AWS-3 — Network Exposure Analysis

The skill SHALL interpret security group and network ACL metadata and identify
unrestricted ingress to sensitive ports. Confirmed weaknesses SHALL be classified as
CWE-284.

---

# AWS-4 — Encryption Analysis

The skill SHALL interpret storage, volume, and database configuration and identify
missing encryption at rest. Confirmed weaknesses SHALL be classified as CWE-311.

---

# AWS-5 — Insecure-Default Analysis

The skill SHALL interpret instance metadata service configuration and other defaults and
identify insecure settings such as permitting the legacy instance metadata service
(IMDSv1). Confirmed weaknesses SHALL be classified as CWE-16.

---

# AWS-6 — Evidence Recording

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
supporting ones to [Evidence](../../../schemas/evidence.md), redacting sensitive values.

---

# Capability Boundaries

The skill SHALL NOT

- Call AWS service APIs directly
- Mutate the environment
- Assess general TLS posture or application-layer weaknesses
- Assess Kubernetes clusters
- Perform destructive exploitation

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to
interface operations in [interface.md](interface.md).
