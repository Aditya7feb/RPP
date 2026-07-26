# Finding Correlation Interface

**File:** `skills/reporting/finding-correlation/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Finding Correlation
Capability.

---

# Operation: correlate

## Request

```yaml
correlate:
  finding_refs:
  correlation:
    deduplicate:
    relate:
    build_chains:
  bounds:
    max_findings:
```

`finding_refs` reference the Findings to correlate. `correlation` selects operations. `bounds`
limits scope.

## Response

```yaml
correlate_result:
  correlation_ref:
  deduplicated_groups:
  related_links:
  attack_chains:
  metrics_ref:
```

`correlation_ref` references correlation content for a [Report](../../../schemas/report.md);
`metrics_ref` references [Metrics](../../../schemas/metrics.md). Results reference Findings by
identifier and contain no new Findings or Risk.

---

# Preconditions

- `finding_refs` SHALL reference existing [Findings](../../../schemas/finding.md).
- `max_findings` SHALL be a positive integer when present.

---

# Postconditions

- Referenced Findings SHALL NOT have been modified.
- Results SHALL reference canonical objects by identifier.
- No new Findings or Risk SHALL be produced.

---

# Error Semantics

Error categories are defined in [error-model.md](error-model.md).

---

# Interface Stability

The `correlate` operation is stable. Additional correlation modes MAY be introduced in a
backward-compatible manner. Consumers SHALL ignore unknown response fields.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
