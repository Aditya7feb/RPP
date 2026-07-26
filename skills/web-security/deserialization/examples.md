# Insecure Deserialization Examples

**File:** `skills/web-security/deserialization/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Insecure
Deserialization Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — Out-Of-Band Confirmation

## Request

```yaml
target: https://app.example.com
payload_set_ref: deser-probes-bounded
collector_ref: oob-collector-controlled
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-deser-5001
    title: Insecure deserialization confirmed by out-of-band interaction
    weakness: CWE-502
    risk_ref: risk-deser-3001
    evidence_refs:
      - evidence-deser-7001
observations:
  - id: obs-deser-4001
    kind: out-of-band-analysis
evidence:
  - id: evidence-deser-7001
    observation_ref: obs-deser-4001
status: completed
metrics:
  endpoints_tested: 3
  findings: 1
```

A bounded serialized probe triggers an interaction to the controlled collector,
confirming unsafe deserialization without delivering a gadget chain.

---

# Example 2 — Differential Indication

## Request

```yaml
target: https://app.example.com
payload_set_ref: deser-probes-bounded
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-deser-5002
    title: Serialized-object processing indicated by response differential
    weakness: CWE-502
    risk_ref: risk-deser-3002
    evidence_refs:
      - evidence-deser-7002
status: completed
metrics:
  endpoints_tested: 3
  findings: 1
```

Response and timing differentials between valid and malformed serialized probes
indicate serialized-object processing, corroborating insecure deserialization.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://app.example.com
payload_set_ref: deser-probes-bounded
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

Deserialization testing is high impact; the Rules of Engagement require approval, so
the skill defers until approval is granted.

---

# Example 4 — Policy Denial

## Request

```yaml
target: https://out-of-scope.example.net
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
- [HTTP Timing Schema](../../../schemas/http-timing.md)
