# Azure Cloud Security Skill Capabilities

**File:** `skills/cloud/azure/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Azure Cloud Security Skill. Each
capability is scope-confined, policy-gated, evidence-backed, and tool independent.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| AZ-1 | Role posture analysis | azure-client metadata | Role Findings |
| AZ-2 | Public exposure analysis | azure-client + cloud-storage-client | Exposure Findings |
| AZ-3 | Network exposure analysis | azure-client metadata | Network Findings |
| AZ-4 | Encryption analysis | azure-client metadata | Encryption Findings |
| AZ-5 | Insecure-default analysis | azure-client metadata | Configuration Findings |
| AZ-6 | Evidence recording | Observations | Evidence references |

---

# AZ-1 — Role Posture Analysis

The skill SHALL interpret observed Entra ID role assignments and effective permissions
and identify over-permissive grants such as broad or subscription-wide privileged roles.
Confirmed weaknesses SHALL be classified as CWE-732 or CWE-269 and referenced to the CIS
Azure Foundations Benchmark identity controls.

---

# AZ-2 — Public Exposure Analysis

The skill SHALL interpret storage access metadata from the
[Cloud Storage Client](../../shared/cloud-storage-client/README.md) and resource metadata
from the [Azure Client](../../shared/azure-client/README.md) and identify public exposure
of storage accounts, containers, and compute resources. Confirmed exposure SHALL be
classified as CWE-284.

---

# AZ-3 — Network Exposure Analysis

The skill SHALL interpret network security group and firewall metadata and identify
unrestricted ingress to sensitive ports. Confirmed weaknesses SHALL be classified as
CWE-284.

---

# AZ-4 — Encryption Analysis

The skill SHALL interpret storage, disk, and database configuration and identify missing
encryption at rest. Confirmed weaknesses SHALL be classified as CWE-311.

---

# AZ-5 — Insecure-Default Analysis

The skill SHALL interpret service configuration and defaults and identify insecure
settings such as exposed management endpoints. Confirmed weaknesses SHALL be classified
as CWE-1188 (Insecure Default Initialization of Resource).

---

# AZ-6 — Evidence Recording

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
supporting ones to [Evidence](../../../schemas/evidence.md), redacting sensitive values.

---

# Capability Boundaries

The skill SHALL NOT

- Call Azure service APIs directly
- Mutate the environment
- Assess general TLS posture or application-layer weaknesses
- Assess Kubernetes clusters
- Perform destructive exploitation

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to
interface operations in [interface.md](interface.md).
