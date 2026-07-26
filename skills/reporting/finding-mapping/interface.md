# Finding Mapping Interface

**File:** `skills/reporting/finding-mapping/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Finding Mapping
Capability.

---

# Operation: map

## Request

```yaml
map:
  finding_refs:
  mapping:
    owasp:
    mitre_attack:
  bounds:
    max_findings:
```

`finding_refs` reference the Findings to map. `mapping` selects frameworks. `bounds` limits scope.

## Response

```yaml
map_result:
  mapping_ref:
  owasp_mappings:
  mitre_attack_mappings:
  metrics_ref:
```

`mapping_ref` references mapping content for a [Report](../../../schemas/report.md); `metrics_ref`
references [Metrics](../../../schemas/metrics.md). Mappings reference Findings by identifier and
contain no new Findings or Risk.

---

# Preconditions

- `finding_refs` SHALL reference existing [Findings](../../../schemas/finding.md).
- `max_findings` SHALL be a positive integer when present.

---

# Postconditions

- Referenced Findings SHALL NOT have been modified.
- Mappings SHALL be presentation enrichment, not authoritative classification changes.
- No new Findings or Risk SHALL be produced.

---

# Error Semantics

Error categories are defined in [error-model.md](error-model.md).

---

# Interface Stability

The `map` operation is stable. Additional frameworks MAY be introduced in a backward-compatible
manner. Consumers SHALL ignore unknown response fields.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
