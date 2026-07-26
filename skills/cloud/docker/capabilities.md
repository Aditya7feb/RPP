# Docker Cloud Security Skill Capabilities

**File:** `skills/cloud/docker/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Docker Cloud Security Skill. Each
capability is scope-confined, policy-gated, evidence-backed, and tool independent.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| DOC-1 | Privilege analysis | container-client metadata | Privilege Findings |
| DOC-2 | Host-exposure analysis | container-client metadata | Host Exposure Findings |
| DOC-3 | Insecure-default analysis | container-client metadata | Configuration Findings |
| DOC-4 | Resource-limit analysis | container-client metadata | Resource Findings |
| DOC-5 | Secret handling analysis | container-client metadata | Secret Findings |
| DOC-6 | Evidence recording | Observations | Evidence references |

---

# DOC-1 — Privilege Analysis

The skill SHALL interpret container privilege and capability configuration and identify
privileged containers or added dangerous capabilities. Confirmed weaknesses SHALL be
classified as CWE-250 and referenced to the CIS Docker Benchmark runtime controls.

---

# DOC-2 — Host-Exposure Analysis

The skill SHALL interpret mount and namespace configuration and identify host daemon socket
or host path mounts and host namespace sharing. Confirmed weaknesses SHALL be classified as
CWE-284.

---

# DOC-3 — Insecure-Default Analysis

The skill SHALL interpret user and default configuration and identify containers configured
to run as the root user. Confirmed weaknesses SHALL be classified as CWE-250.

---

# DOC-4 — Resource-Limit Analysis

The skill SHALL interpret resource configuration and identify missing CPU or memory limits.
Confirmed weaknesses SHALL be classified as CWE-770.

---

# DOC-5 — Secret Handling Analysis

The skill SHALL interpret image and container configuration and identify secrets embedded in
image layers or environment. Confirmed weaknesses SHALL be classified as CWE-312.

---

# DOC-6 — Evidence Recording

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
supporting ones to [Evidence](../../../schemas/evidence.md), redacting sensitive values.

---

# Capability Boundaries

The skill SHALL NOT

- Call the container engine directly
- Mutate the platform or execute containers
- Assess Kubernetes clusters, TLS posture, or application-layer weaknesses
- Perform destructive exploitation

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface
operations in [interface.md](interface.md).
