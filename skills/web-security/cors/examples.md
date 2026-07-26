# CORS Examples

**File:** `skills/web-security/cors/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the CORS Skill.
Examples illustrate the interface and outputs; they contain no implementation code.

---

# Example 1 — Arbitrary Origin Reflected With Credentials

## Request

```yaml
target: https://api.example.com
test_origins:
  - https://attacker.example
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-cors-5001
    title: Arbitrary origin reflected with credentialed access allowed
    weakness: CWE-942
    risk_ref: risk-cors-3001
    evidence_refs:
      - evidence-cors-7001
observations:
  - id: obs-cors-4001
    kind: origin-reflection-analysis
evidence:
  - id: evidence-cors-7001
    observation_ref: obs-cors-4001
status: completed
metrics:
  checks_performed: 6
  findings: 1
```

The API reflects the attacker-supplied `Origin` into `Access-Control-Allow-Origin`
and returns `Access-Control-Allow-Credentials: true`, enabling cross-origin theft of
authenticated responses.

---

# Example 2 — Null Origin Accepted

## Request

```yaml
target: https://api.example.com
test_origins:
  - "null"
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-cors-5002
    title: Null origin accepted as trusted
    weakness: CWE-942
    risk_ref: risk-cors-3002
    evidence_refs:
      - evidence-cors-7002
status: completed
metrics:
  checks_performed: 6
  findings: 1
```

The API accepts the `null` origin, which sandboxed documents can send, allowing
untrusted contexts to read responses.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://api.example.com
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

The Rules of Engagement require approval before active probing; the skill defers
until approval is granted.

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
- [HTTP Header Schema](../../../schemas/http-header.md)
