# Server-Side Template Injection Examples

**File:** `skills/web-security/ssti/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Server-Side
Template Injection Skill. Examples illustrate the interface and outputs; they contain
no implementation code.

---

# Example 1 — Expression Marker Evaluated

## Request

```yaml
target: https://app.example.com
payload_set_ref: ssti-markers-bounded
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-ssti-5001
    title: Server-side template injection in name parameter
    weakness: CWE-1336
    risk_ref: risk-ssti-3001
    evidence_refs:
      - evidence-ssti-7001
observations:
  - id: obs-ssti-4001
    kind: expression-evaluation-analysis
evidence:
  - id: evidence-ssti-7001
    observation_ref: obs-ssti-4001
    marker: bounded-arithmetic
status: completed
metrics:
  injection_points_tested: 6
  findings: 1
```

A bounded arithmetic expression injected into the `name` parameter is evaluated and
returns its computed result, confirming template injection without code execution.

---

# Example 2 — Engine Class Indicated

## Request

```yaml
target: https://app.example.com
payload_set_ref: ssti-markers-bounded
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-ssti-5002
    title: Template injection with engine class indicated
    weakness: CWE-1336
    risk_ref: risk-ssti-3002
    evidence_refs:
      - evidence-ssti-7002
status: completed
metrics:
  injection_points_tested: 6
  findings: 1
```

Evaluation behavior indicates a specific template engine class, informing
exploitability while remaining within bounded expression evaluation.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://app.example.com
payload_set_ref: ssti-markers-bounded
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

Template injection testing is high impact; the Rules of Engagement require approval,
so the skill defers until approval is granted.

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
