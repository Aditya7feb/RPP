# SQL Injection Examples

**File:** `skills/web-security/sqli/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the SQL Injection
Skill. Examples illustrate the interface and outputs; they contain no implementation
code.

---

# Example 1 — Error-Based SQL Injection

## Request

```yaml
target: https://app.example.com
payload_set_ref: sqli-probes-bounded
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-sqli-5001
    title: Error-based SQL injection in id parameter
    weakness: CWE-89
    risk_ref: risk-sqli-3001
    evidence_refs:
      - evidence-sqli-7001
observations:
  - id: obs-sqli-4001
    kind: error-signal-analysis
evidence:
  - id: evidence-sqli-7001
    observation_ref: obs-sqli-4001
status: completed
metrics:
  injection_points_tested: 8
  findings: 1
```

A malformed value in the `id` parameter produces a database error, confirming
error-based injection without extracting data.

---

# Example 2 — Time-Based Blind SQL Injection

## Request

```yaml
target: https://app.example.com
payload_set_ref: sqli-probes-bounded
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-sqli-5002
    title: Time-based blind SQL injection in filter parameter
    weakness: CWE-89
    risk_ref: risk-sqli-3002
    evidence_refs:
      - evidence-sqli-7002
status: completed
metrics:
  injection_points_tested: 8
  findings: 1
```

A bounded conditional delay induced through the `filter` parameter is observed
repeatedly, confirming time-based blind injection without data extraction.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://app.example.com
payload_set_ref: sqli-probes-bounded
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

The Rules of Engagement require approval before active injection probing; the skill
defers until approval is granted.

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
