# API Key Authentication Examples

**File:** `skills/authentication/api-keys/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the API Key
Authentication Skill. Examples illustrate the interface and outputs; they contain
no implementation code.

---

# Example 1 — Key In Query String

## Request

```yaml
target: https://api.example.com
api_key_ref: apikey-example-tester
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-akey-5001
    title: API key transmitted in query string
    risk_ref: risk-akey-3001
    evidence_refs:
      - evidence-akey-7001
observations:
  - id: obs-akey-4001
    kind: key-placement-analysis
evidence:
  - id: evidence-akey-7001
    observation_ref: obs-akey-4001
    redacted: true
status: completed
metrics:
  checks_performed: 5
  findings: 1
```

The API is authenticated by a key placed in the query string, exposing it in logs
and history. The weakness is reported with redacted Evidence.

---

# Example 2 — Key Exposed In Client Code

## Request

```yaml
target: https://app.example.com
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-akey-5002
    title: API key embedded in client-side JavaScript
    risk_ref: risk-akey-3002
    evidence_refs:
      - evidence-akey-7002
status: completed
metrics:
  checks_performed: 5
  findings: 1
```

A usable key is present in client-side code. Evidence redacts the key value.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://api.example.com
api_key_ref: apikey-example-tester
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

The Rules of Engagement require approval for active key validation testing; the
skill defers until approval is granted.

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
- [Asset Schema](../../../schemas/asset.md)
