# CSRF Protection Examples

**File:** `skills/authentication/csrf/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the CSRF
Protection Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — Missing Anti-CSRF Token

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
  - id: finding-csrf-5001
    title: State-changing endpoint requires no anti-CSRF token
    risk_ref: risk-csrf-3001
    evidence_refs:
      - evidence-csrf-7001
observations:
  - id: obs-csrf-4001
    kind: token-presence-analysis
evidence:
  - id: evidence-csrf-7001
    observation_ref: obs-csrf-4001
    redacted: true
status: completed
metrics:
  checks_performed: 6
  findings: 1
```

A profile-update endpoint accepts state changes without any anti-CSRF token. The
weakness is confirmed without executing a harmful change.

---

# Example 2 — Token Not Validated

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
  - id: finding-csrf-5002
    title: Anti-CSRF token is present but not validated
    risk_ref: risk-csrf-3002
    evidence_refs:
      - evidence-csrf-7002
status: completed
metrics:
  checks_performed: 6
  findings: 1
```

The server accepts a request with an altered token, indicating the token is not
validated. Evidence redacts token values.

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

The Rules of Engagement require approval before testing state-changing endpoints;
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
- [HTTP Cookie Schema](../../../schemas/http-cookie.md)
