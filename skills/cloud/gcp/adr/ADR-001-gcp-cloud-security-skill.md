# ADR-001 — GCP Cloud Security Skill

**File:** `skills/cloud/gcp/adr/ADR-001-gcp-cloud-security-skill.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

The RPP platform assesses GCP environments for security posture weaknesses spanning
identity and access (IAM policy bindings), public exposure, encryption, and insecure
defaults. These concerns require interpreting provider-native GCP metadata — IAM bindings,
firewall rules, storage configuration, and service-account settings — against recognized
benchmarks.

The GCP Client and Cloud Storage Client shared skills provide confined, read-preferring
access to provider-native metadata but deliberately perform no interpretation and produce
no findings. A dedicated domain skill is required to interpret that metadata, classify
weaknesses, and emit evidence-backed findings, while never calling provider APIs directly,
never mutating the environment, and delegating TLS posture and application-layer weaknesses
to their respective tiers.

---

# Decision

We SHALL provide a GCP Cloud Security Skill in the Cloud Security tier with the following
properties.

- It consumes provider-native metadata through the
  [GCP Client](../../../shared/gcp-client/README.md) and storage exposure metadata through
  the [Cloud Storage Client](../../../shared/cloud-storage-client/README.md), and SHALL NOT
  call provider APIs directly.
- It consults the [Policy Engine](../../../shared/policy-engine/README.md) before every
  target-facing action.
- It interprets IAM, exposure, encryption, and insecure-default posture and classifies
  weaknesses using CWE identifiers aligned to the CIS GCP Foundations Benchmark.
- It produces and enriches `cloud-resource` [Assets](../../../../schemas/asset.md) and
  emits [Findings](../../../../schemas/finding.md) with
  [Risk](../../../../schemas/risk.md), each backed by
  [Evidence](../../../../schemas/evidence.md).
- It does not mutate the environment and delegates TLS posture to TLS Analysis, application
  weaknesses to Web Security skills, and cluster assessment to the Kubernetes Cloud Security
  skill.

---

# Consequences

## Positive

- GCP posture interpretation is centralized in a cohesive, tool-independent skill.
- Interpretation is cleanly separated from the shared clients that only report metadata.
- Findings are evidence-backed and benchmark-aligned.

## Negative

- The skill depends on the breadth of metadata the shared clients expose.

## Neutral

- Organization-policy aggregation and drift detection are deferred to future extensions.

---

# Alternatives Considered

- Interpreting GCP posture inside the GCP Client. Rejected because the shared client reports
  metadata as data and must not embed security interpretation.
- A single provider-agnostic cloud skill. Rejected because GCP resource models and
  benchmarks are provider-specific and would lose fidelity.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [GCP Client](../../../shared/gcp-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
