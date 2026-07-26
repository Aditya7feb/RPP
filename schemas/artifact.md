# Artifact Schema

**File:** `schemas/artifact.md`

**Version:** 1.0.0

---

# Purpose

The Artifact Schema defines the canonical, implementation-independent representation of a
stored output produced during an assessment within the Robust PenTest Platform (RPP).

An Artifact is a referenced, durable output such as a recorded traffic capture, a response
corpus, a replay log, or a comparison result. Artifacts carry produced data by reference so
that capabilities can exchange large outputs without inlining them.

An Artifact represents produced data only. It SHALL NOT contain security interpretation,
findings, risk, or secrets. Interpretation of an Artifact is deferred to domain
capabilities.

---

# Design Principles

An Artifact SHALL be

- Referenced rather than inlined
- Traceable to its producing capability
- Integrity-verifiable
- Immutable once recorded
- Redacted of sensitive content
- Auditable
- Implementation independent

---

# Identity

Every Artifact SHALL contain

```yaml
artifact_id:

assessment_id:

task_id:

schema_version:
```

`artifact_id` SHALL be unique within an assessment. `assessment_id` SHALL reference the
owning [assessment](assessment.md). `task_id` SHALL reference the producing
[task](task.md). `schema_version` SHALL be `1.0.0`.

---

# Classification

Every Artifact SHALL contain

```yaml
classification:
  type:
  format:
```

`type` SHALL name the artifact kind, such as `traffic-recording`, `response-capture`,
`payload-corpus`, `replay-log`, `traffic-diff`, or `coverage-map`. `format` SHALL name the
logical format, such as `har`, `pcap-reference`, `ndjson`, or `structured-record`.

---

# Location And Integrity

Every Artifact SHALL contain

```yaml
storage:
  location_ref:
  size_bytes:
  content_hash:
  redacted:
```

`location_ref` SHALL reference where the Artifact is stored; content SHALL NOT be inlined.
`size_bytes` SHALL record the stored size. `content_hash` SHALL provide an integrity value.
`redacted` SHALL indicate whether sensitive content was removed.

---

# Provenance

Every Artifact SHALL contain

```yaml
provenance:
  produced_by:
  produced_at:
  inputs:
```

`produced_by` SHALL name the producing capability. `produced_at` SHALL record production
time. `inputs` MAY reference the [Payloads](payload.md), Artifacts, or Observations that
contributed to it.

---

# Required Fields

An Artifact SHALL define `artifact_id`, `assessment_id`, `task_id`, `schema_version`,
`classification.type`, `storage.location_ref`, and `provenance.produced_by`.

---

# Validation Rules

- `artifact_id` SHALL be unique within an assessment.
- `storage.location_ref` SHALL resolve to stored content; content SHALL NOT be inlined.
- `content_hash` SHOULD be present to support integrity verification.
- Sensitive content SHALL be redacted or referenced, never inlined in the Artifact record.
- Unknown optional fields SHALL be ignored for forward compatibility.

---

# Relationships

- An Artifact MAY be promoted to or referenced by [Evidence](evidence.md).
- An Artifact MAY reference [Payloads](payload.md) and [Observations](observation.md) as
  inputs.
- An Artifact SHALL NOT reference [Findings](finding.md) or [Risk](risk.md); interpretation
  belongs to domain capabilities.

---

# Example Object

```yaml
artifact_id: artifact-8001
assessment_id: assessment-2024-014
task_id: task-3120
schema_version: 1.0.0
classification:
  type: traffic-recording
  format: har
storage:
  location_ref: store://artifacts/8001
  size_bytes: 481203
  content_hash: sha256:5f2c...e91a
  redacted: true
provenance:
  produced_by: traffic-recording
  produced_at: "2026-07-26T14:12:07Z"
  inputs:
    - task-3120
```

---

# Extension Points

- Additional `classification.type` and `format` values MAY be introduced.
- `provenance` MAY be extended with additional lineage metadata.
- Consumers SHALL ignore unknown optional fields.

---

# Versioning Notes

`schema_version` SHALL follow semantic versioning. Backward-compatible additions increment
the minor version. Unknown optional fields SHALL be ignored by consumers.
