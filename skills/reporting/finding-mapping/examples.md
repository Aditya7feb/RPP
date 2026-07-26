# Finding Mapping Examples

**File:** `skills/reporting/finding-mapping/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Finding Mapping Capability.

---

# Example 1 — Map To OWASP And ATT&CK

## Request

```yaml
map:
  finding_refs:
    - finding-sqli-5001
    - finding-xss-5002
  mapping:
    owasp: true
    mitre_attack: true
  bounds:
    max_findings: 500
```

## Response

```yaml
map_result:
  mapping_ref: mapping-rp-9201
  owasp_mappings:
    - finding: finding-sqli-5001
      owasp: "A03:2021 - Injection"
    - finding: finding-xss-5002
      owasp: "A03:2021 - Injection"
  mitre_attack_mappings:
    - finding: finding-sqli-5001
      technique: "T1190 - Exploit Public-Facing Application"
  metrics_ref: metrics-rp-7201
```

The capability enriches Findings with OWASP and MITRE ATT&CK mappings for presentation, referencing
Findings by identifier and leaving their canonical classification unchanged.

---

# Example 2 — Unmappable Finding

## Response

```yaml
map_result:
  mapping_ref: mapping-rp-9202
  owasp_mappings:
    - finding: finding-info-5030
      owasp: unmapped
  metrics_ref: metrics-rp-7202
```

A Finding lacks attributes required to map to a framework, so it is recorded as unmapped rather than
receiving an invented mapping.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
