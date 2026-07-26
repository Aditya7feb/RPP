# Evidence Bundle Examples

**File:** `skills/reporting/evidence-bundle/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Evidence Bundle Capability.

---

# Example 1 — Bundle A Report's Evidence

## Request

```yaml
bundle:
  evidence_refs:
    - evidence-ev-8101
    - evidence-ev-8201
    - evidence-ev-8301
  finding_refs:
    - finding-sqli-5001
  redaction:
    redact_sensitive: true
  bounds:
    max_evidence: 500
    max_size_bytes: 104857600
```

## Response

```yaml
bundle_result:
  bundle_artifact_ref: artifact-rp-9701
  evidence_count: 3
  integrity_verified: true
  metrics_ref: metrics-rp-7701
```

The capability assembles the referenced Evidence into an integrity-verified, redacted
`evidence-bundle` Artifact, referencing Evidence by identifier and leaving it unchanged.

---

# Example 2 — Integrity Failure Excluded

## Request

```yaml
bundle:
  evidence_refs:
    - evidence-ev-8101
    - evidence-ev-8888
  bounds:
    max_evidence: 500
```

## Response

```yaml
bundle_result:
  bundle_artifact_ref: artifact-rp-9702
  evidence_count: 1
  integrity_verified: partial
  metrics_ref: metrics-rp-7702
```

One Evidence object failed integrity verification and is excluded; the failure is recorded in the
bundle metadata.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
