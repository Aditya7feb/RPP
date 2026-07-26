# Cloud Capability Tier

**File:** `skills/cloud/README.md`

**Version:** 1.0.0

---

# Purpose

The Cloud tier provides reusable, implementation-independent capabilities that
analyze cloud and container security posture within the Robust PenTest Platform
(RPP). These capabilities produce Observations, Findings, and Evidence references
across cloud providers and container platforms.

This tier comprises the following capabilities.

- [AWS](aws/README.md)
- [Azure](azure/README.md)
- [GCP](gcp/README.md)
- [Kubernetes](kubernetes/README.md)
- [Docker](docker/README.md)
- [Terraform](terraform/README.md)

---

# Ownership Boundary

Cloud capabilities analyze configuration and posture and produce Findings and
Evidence references. They operate within authenticated cloud boundaries defined by
scope and Rules of Engagement. State-changing validation is owned by the Active
Testing tier and requires human approval.

---

# Role in the Canonical Pipeline

Cloud capabilities contribute Observations, Evidence, and Findings to the pipeline
**Observation → Evidence → Finding → Risk → Recommendation**.

---

# Canonical Schemas

Cloud capabilities consume and produce
[observation](../../schemas/observation.md),
[finding](../../schemas/finding.md), and
[evidence](../../schemas/evidence.md), and reference
[asset](../../schemas/asset.md),
[scope](../../schemas/scope.md), and
[rules-of-engagement](../../schemas/rules-of-engagement.md).

---

# Related

- Orchestrated by the [Cloud Agent](../../agents/cloud/README.md).
- Shared infrastructure under [skills/shared](../shared/README.md).
