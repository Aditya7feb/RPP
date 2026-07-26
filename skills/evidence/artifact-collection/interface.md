# Artifact Collection Interface

**File:** `skills/evidence/artifact-collection/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Artifact Collection
Capability.

---

# Operation: collect

## Request

```yaml
collect:
  sources:
  types:
  bounds:
    max_artifacts:
    max_size_bytes:
  redaction:
  scope_id:
  roe_id:
```

`sources` reference authorized locations. `types` selects artifact types. `bounds` limits
collection.

## Response

```yaml
collect_result:
  artifact_refs:
  artifact_count:
  evidence_refs:
  metrics_ref:
```

`artifact_refs` reference [Artifacts](../../../schemas/artifact.md); `evidence_refs` reference
[Evidence](../../../schemas/evidence.md) produced through the shared lifecycle; `metrics_ref`
references [Metrics](../../../schemas/metrics.md). No Findings or Risk are produced.

---

# Preconditions

- `sources` SHALL reference authorized locations within the assessment
  [Scope](../../../schemas/scope.md).
- `max_artifacts` SHALL be a positive integer when present.

---

# Postconditions

- Only authorized locations SHALL have been collected.
- Sensitive content SHALL have been redacted where configured.
- Collection SHALL have remained bounded.

---

# Error Semantics

Error categories are defined in [error-model.md](error-model.md).

---

# Interface Stability

The `collect` operation is stable. Additional types and selection modes MAY be introduced in a
backward-compatible manner. Consumers SHALL ignore unknown response fields.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
