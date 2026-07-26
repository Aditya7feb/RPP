# Discovery Capability Tier

**File:** `skills/discovery/README.md`

**Version:** 1.0.0

---

# Purpose

The Discovery tier provides reusable, implementation-independent capabilities that
enumerate the attack surface of an authorized target within the Robust PenTest
Platform (RPP). Discovery capabilities observe and enumerate; they produce
Observations and asset references and do not confirm vulnerabilities.

This tier comprises the following capabilities.

- [Asset Discovery](asset-discovery/README.md)
- [Subdomain Discovery](subdomain-discovery/README.md)
- [DNS Enumeration](dns-enumeration/README.md)
- [Port Discovery](port-discovery/README.md)
- [Virtual Host Discovery](virtual-host-discovery/README.md)
- [Fingerprinting](fingerprinting/README.md)
- [Content Discovery](content-discovery/README.md)
- [Endpoint Enumeration](endpoint-enumeration/README.md)
- [API Discovery](api-discovery/README.md)
- [TLS Analysis](tls-analysis/README.md)
- [Recon](recon/README.md)

---

# Ownership Boundary

Discovery capabilities produce Observations and asset references. They SHALL NOT
produce canonical Risk, and they SHALL NOT perform payload-driven validation,
which is owned by the Active Testing tier under human approval.

---

# Role in the Canonical Pipeline

Discovery sits at the head of the pipeline: **Observation → Evidence → Finding →
Risk → Recommendation**. Its Observations and assets inform which downstream
capability tiers apply to the target.

---

# Canonical Schemas

Discovery capabilities consume and produce
[asset](../../schemas/asset.md),
[asset-relationship](../../schemas/asset-relationship.md),
[observation](../../schemas/observation.md), and
[technology](../../schemas/technology.md), and reference
[scope](../../schemas/scope.md) and
[rules-of-engagement](../../schemas/rules-of-engagement.md).

---

# Related

- Orchestrated by the [Discovery Agent](../../agents/discovery/README.md).
- Shared infrastructure under [skills/shared](../shared/README.md).
