# Endpoint Enumeration Examples

**File:** `skills/discovery/endpoint-enumeration/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Endpoint
Enumeration Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — Rendered And Script Extraction

## Request

```yaml
target: https://app.example.com
mine_parameters: false
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
endpoints:
  - id: endpoint-ee-9001
    type: endpoint
    value: https://app.example.com/api/orders
    parameters:
      - name: status
        source: observed
        confidence: high
      - name: page
        source: observed
        confidence: high
    scope_status: in-scope
    provenance:
      observation_ref: obs-ee-4001
relationships:
  - type: references
    from: endpoint-ee-9001
    to: asset-app-example
observations:
  - id: obs-ee-4001
    kind: script-extraction
evidence:
  - id: evidence-ee-7001
    observation_ref: obs-ee-4001
findings: []
status: completed
metrics:
  endpoints_enriched: 1
  parameters_found: 2
```

Endpoints and parameters are extracted from rendered content and scripts. No
mining is performed.

---

# Example 2 — Parameter Mining Reveals A Hidden Parameter

## Request

```yaml
target: https://app.example.com
mine_parameters: true
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
endpoints:
  - id: endpoint-ee-9002
    type: endpoint
    value: https://app.example.com/api/orders
    parameters:
      - name: debug
        source: mined
        confidence: medium
        behavior_changed: true
    scope_status: in-scope
findings:
  - id: finding-ee-5001
    title: Hidden parameter alters application behavior
    risk_ref: risk-ee-3001
    evidence_refs:
      - evidence-ee-7002
status: completed
metrics:
  endpoints_enriched: 1
  parameters_found: 1
  findings: 1
```

A mined `debug` parameter changes behavior and is reported as a Finding with Risk,
backed by Evidence. The parameter is not tested for vulnerabilities.

---

# Example 3 — Policy Denial

## Request

```yaml
target: https://out-of-scope.example.net
mine_parameters: true
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
endpoints: []
findings: []
status: denied
metrics:
  policy_denials: 1
```

The target is out of scope. The Policy Engine denies the action and the skill
performs no enumeration.

---

# Example 4 — Partial Due To Rate Ceiling

## Request

```yaml
target: https://app.example.com
mine_parameters: true
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
endpoints:
  - id: endpoint-ee-9003
    type: endpoint
    value: https://app.example.com/api/reports
status: partial
metrics:
  endpoints_enriched: 1
  rate_limited: true
```

The policy rate ceiling is reached; the skill paces remaining actions and returns
partial results with Evidence.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Asset Schema](../../../schemas/asset.md)
