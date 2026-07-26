# ADR-001 — Docker Cloud Security Skill

**File:** `skills/cloud/docker/adr/ADR-001-docker-cloud-security-skill.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

The RPP platform assesses container platforms for security posture weaknesses spanning
privileged execution, host exposure, insecure defaults, resource limits, and embedded
secrets. These concerns require interpreting provider-native container metadata — image
manifests, container settings, daemon configuration, and runtime capabilities — against
recognized benchmarks.

The Container Client shared skill provides confined, read-preferring access to
provider-native container metadata but deliberately performs no interpretation and produces
no findings. A dedicated domain skill is required to interpret that metadata, classify
weaknesses, and emit evidence-backed findings, while never calling the container engine
directly, never mutating the platform or executing containers, and delegating cluster
assessment, TLS posture, and application-layer weaknesses to their respective tiers.

---

# Decision

We SHALL provide a Docker Cloud Security Skill in the Cloud Security tier with the following
properties.

- It consumes provider-native metadata through the
  [Container Client](../../../shared/container-client/README.md) and SHALL NOT call the
  container engine directly.
- It consults the [Policy Engine](../../../shared/policy-engine/README.md) before every
  target-facing action.
- It interprets privilege, host-exposure, insecure-default, resource-limit, and secret
  posture and classifies weaknesses using CWE identifiers aligned to the CIS Docker
  Benchmark.
- It produces and enriches `cloud-resource` [Assets](../../../../schemas/asset.md) and emits
  [Findings](../../../../schemas/finding.md) with [Risk](../../../../schemas/risk.md), each
  backed by [Evidence](../../../../schemas/evidence.md).
- It does not mutate the platform or execute containers and delegates cluster assessment to
  the Kubernetes skill, TLS posture to TLS Analysis, and application weaknesses to Web
  Security skills.

---

# Consequences

## Positive

- Container posture interpretation is centralized in a cohesive, tool-independent skill.
- Interpretation is cleanly separated from the shared client that only reports metadata.
- Findings are evidence-backed and benchmark-aligned.

## Negative

- The skill depends on the breadth of metadata the shared client exposes.

## Neutral

- Image provenance and runtime security-profile posture are deferred to future extensions.

---

# Alternatives Considered

- Interpreting container posture inside the Container Client. Rejected because the shared
  client reports metadata as data and must not embed security interpretation.
- Assessing containers within the Kubernetes skill. Rejected because standalone container
  platforms are distinct from clusters and warrant a dedicated skill.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [Container Client](../../../shared/container-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
