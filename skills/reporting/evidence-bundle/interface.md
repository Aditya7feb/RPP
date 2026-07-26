# Evidence Bundle Interface

**File:** `skills/reporting/evidence-bundle/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Evidence Bundle
Capability.

---

# Operation: bundle

## Request

```yaml
bundle:
  evidence_refs:
  finding_refs:
  redaction:
  bounds:
    max_evidence:
    max_size_bytes:
```

`evidence_refs` reference the Evidence to bundle. `finding_refs` MAY scope the bundle. `redaction`
configures distribution redaction. `bounds` limits bundle size.

## Response

```yaml
bundle_result:
  bundle_artifact_ref:
  evidence_count:
  integrity_verified:
  metrics_ref:
```

`bundle_artifact_ref` references a bundle [Artifact](../../../schemas/artifact.md) of type
`evidence-bundle`; `metrics_ref` references [Metrics](../../../schemas/metrics.md). The bundle
references Evidence by identifier and contains no new Findings or Risk.

---

# Preconditions

- `evidence_refs` SHALL reference existing [Evidence](../../../schemas/evidence.md).
- `max_evidence` SHALL be a positive integer when present.

---

# Postconditions

- Referenced Evidence SHALL NOT have been modified.
- Integrity references SHALL have been preserved.
- Sensitive content SHALL have been redacted where required.

---

# Error Semantics

Error categories are defined in [error-model.md](error-model.md).

---

# Interface Stability

The `bundle` operation is stable. Additional bundle options MAY be introduced in a
backward-compatible manner. Consumers SHALL ignore unknown response fields.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
