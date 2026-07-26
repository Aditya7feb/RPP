# Cross-Site Scripting Examples

**File:** `skills/web-security/xss/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Cross-Site
Scripting Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — Reflected XSS

## Request

```yaml
target: https://app.example.com
payload_set_ref: xss-markers-bounded
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-xss-5001
    title: Reflected XSS in search parameter
    weakness: CWE-79
    risk_ref: risk-xss-3001
    evidence_refs:
      - evidence-xss-7001
observations:
  - id: obs-xss-4001
    kind: context-encoding-analysis
evidence:
  - id: evidence-xss-7001
    observation_ref: obs-xss-4001
    marker: rpp-marker-9f3a
status: completed
metrics:
  injection_points_tested: 12
  findings: 1
```

The `q` parameter is reflected into an HTML context without encoding; the bounded
marker executes in a rendered context, confirming reflected XSS.

---

# Example 2 — DOM-Based XSS

## Request

```yaml
target: https://app.example.com
payload_set_ref: xss-markers-bounded
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-xss-5002
    title: DOM-based XSS via fragment passed to a dangerous sink
    weakness: CWE-79
    risk_ref: risk-xss-3002
    evidence_refs:
      - evidence-xss-7002
status: completed
metrics:
  injection_points_tested: 12
  findings: 1
```

Client-side code passes the URL fragment to a dangerous sink; the bounded marker
executes in the DOM, confirming DOM-based XSS.

---

# Example 3 — Stored XSS Requires Approval

## Request

```yaml
target: https://app.example.com
payload_set_ref: xss-markers-bounded
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

Stored-XSS testing persists input and is higher impact; the Rules of Engagement
require approval, so the skill defers until approval is granted.

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
- [Browser](../../shared/browser/README.md)
