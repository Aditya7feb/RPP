# GCP Cloud Security Skill Capabilities

**File:** `skills/cloud/gcp/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the GCP Cloud Security Skill. Each capability
is scope-confined, policy-gated, evidence-backed, and tool independent.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| GCP-1 | IAM posture analysis | gcp-client metadata | IAM Findings |
| GCP-2 | Public exposure analysis | gcp-client + cloud-storage-client | Exposure Findings |
| GCP-3 | Network exposure analysis | gcp-client metadata | Network Findings |
| GCP-4 | Encryption analysis | gcp-client metadata | Encryption Findings |
| GCP-5 | Insecure-default analysis | gcp-client metadata | Configuration Findings |
| GCP-6 | Evidence recording | Observations | Evidence references |

---

# GCP-1 — IAM Posture Analysis

The skill SHALL interpret observed IAM policy bindings and effective permissions and
identify over-permissive grants such as primitive roles (Owner, Editor) or public
principals (`allUsers`, `allAuthenticatedUsers`). Confirmed weaknesses SHALL be classified
as CWE-732 or CWE-269 and referenced to the CIS GCP Foundations Benchmark identity
controls.

---

# GCP-2 — Public Exposure Analysis

The skill SHALL interpret storage access metadata from the
[Cloud Storage Client](../../shared/cloud-storage-client/README.md) and resource metadata
from the [GCP Client](../../shared/gcp-client/README.md) and identify public exposure of
buckets, objects, and compute resources. Confirmed exposure SHALL be classified as
CWE-284.

---

# GCP-3 — Network Exposure Analysis

The skill SHALL interpret firewall rule metadata and identify unrestricted ingress to
sensitive ports. Confirmed weaknesses SHALL be classified as CWE-284.

---

# GCP-4 — Encryption Analysis

The skill SHALL interpret storage, disk, and database configuration and identify missing
encryption assurances at rest. Confirmed weaknesses SHALL be classified as CWE-311.

---

# GCP-5 — Insecure-Default Analysis

The skill SHALL interpret service account, metadata-server, and other default
configuration and identify insecure settings such as default service accounts with broad
scopes. Confirmed weaknesses SHALL be classified as CWE-16.

---

# GCP-6 — Evidence Recording

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
supporting ones to [Evidence](../../../schemas/evidence.md), redacting sensitive values.

---

# Capability Boundaries

The skill SHALL NOT

- Call GCP service APIs directly
- Mutate the environment
- Assess general TLS posture or application-layer weaknesses
- Assess Kubernetes clusters
- Perform destructive exploitation

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface
operations in [interface.md](interface.md).
