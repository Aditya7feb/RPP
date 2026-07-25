# Session Management Examples

**File:** `skills/authentication/sessions/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Session
Management Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — Insecure Cookie Attributes

## Request

```yaml
target: https://app.example.com
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-sess-5001
    title: Session cookie missing HttpOnly and Secure attributes
    risk_ref: risk-sess-3001
    evidence_refs:
      - evidence-sess-7001
observations:
  - id: obs-sess-4001
    kind: cookie-attribute-analysis
evidence:
  - id: evidence-sess-7001
    observation_ref: obs-sess-4001
    redacted: true
status: completed
metrics:
  checks_performed: 6
  findings: 1
```

The session cookie lacks `HttpOnly` and `Secure`; the weakness is reported with
Risk and redacted Evidence.

---

# Example 2 — Session Fixation

## Request

```yaml
target: https://app.example.com
credentials_ref: creds-example-tester
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-sess-5002
    title: Session identifier not rotated after authentication
    risk_ref: risk-sess-3002
    evidence_refs:
      - evidence-sess-7002
status: completed
metrics:
  checks_performed: 6
  findings: 1
```

The identifier issued before login remains valid after authentication, indicating
session fixation. Evidence redacts the identifier value.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://app.example.com
credentials_ref: creds-example-tester
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

The Rules of Engagement require approval for authenticated session testing; the
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
- [HTTP Cookie Schema](../../../schemas/http-cookie.md)
