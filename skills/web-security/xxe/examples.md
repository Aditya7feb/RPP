# XML External Entity Examples

**File:** `skills/web-security/xxe/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the XML External
Entity Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — In-Band Resolution With Non-Sensitive Marker

## Request

```yaml
target: https://api.example.com/xml
marker_ref: benign-marker-resource
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-xxe-5001
    title: XML external entity resolution in XML endpoint
    weakness: CWE-611
    risk_ref: risk-xxe-3001
    evidence_refs:
      - evidence-xxe-7001
observations:
  - id: obs-xxe-4001
    kind: in-band-resolution-analysis
evidence:
  - id: evidence-xxe-7001
    observation_ref: obs-xxe-4001
status: completed
metrics:
  endpoints_tested: 3
  findings: 1
```

The XML endpoint resolves a bounded, non-sensitive external entity, confirming XXE
without reading a sensitive file.

---

# Example 2 — Out-Of-Band Resolution

## Request

```yaml
target: https://api.example.com/xml
collector_ref: oob-collector-controlled
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-xxe-5002
    title: Blind XXE confirmed by out-of-band interaction
    weakness: CWE-611
    risk_ref: risk-xxe-3002
    evidence_refs:
      - evidence-xxe-7002
status: completed
metrics:
  endpoints_tested: 3
  findings: 1
```

An external entity triggers an interaction to the controlled collector, confirming
blind XXE out-of-band.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://api.example.com/xml
marker_ref: benign-marker-resource
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings: []
status: awaiting_approval
metrics:
  approvals_requested: 1
```

XXE testing is high impact; the Rules of Engagement require approval, so the skill
defers until approval is granted.

---

# Example 4 — Policy Denial

## Request

```yaml
target: https://out-of-scope.example.net/xml
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings: []
status: denied
metrics:
  policy_denials: 1
```

The target is out of scope. The Policy Engine denies the action and no testing is
performed.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Asset Schema](../../../schemas/asset.md)
