# JWT Authentication Examples

**File:** `skills/authentication/jwt/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the JWT
Authentication Skill. Examples illustrate the interface and outputs; they contain
no implementation code.

---

# Example 1 — Unsigned Token Accepted

## Request

```yaml
target: https://api.example.com
token_ref: token-example-tester
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-jwt-5001
    title: Server accepts unsigned tokens (alg none)
    risk_ref: risk-jwt-3001
    evidence_refs:
      - evidence-jwt-7001
observations:
  - id: obs-jwt-4001
    kind: signature-validation-analysis
evidence:
  - id: evidence-jwt-7001
    observation_ref: obs-jwt-4001
    redacted: true
status: completed
metrics:
  checks_performed: 7
  findings: 1
```

A token with `alg` set to `none` is accepted, indicating signatures are not
enforced. Evidence redacts token material.

---

# Example 2 — Algorithm Confusion

## Request

```yaml
target: https://api.example.com
token_ref: token-example-tester
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-jwt-5002
    title: Asymmetric public key accepted as HMAC secret
    risk_ref: risk-jwt-3002
    evidence_refs:
      - evidence-jwt-7002
status: completed
metrics:
  checks_performed: 7
  findings: 1
```

The server verifies an `HS256` token using the public key intended for `RS256`,
indicating algorithm confusion. Evidence redacts token material.

---

# Example 3 — Sensitive Payload Data

## Request

```yaml
target: https://api.example.com
token_ref: token-example-tester
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-jwt-5003
    title: Sensitive personal data disclosed in token payload
    risk_ref: risk-jwt-3003
    evidence_refs:
      - evidence-jwt-7003
status: completed
metrics:
  checks_performed: 7
  findings: 1
```

The token payload discloses sensitive fields. Evidence records the finding with the
sensitive values redacted.

---

# Example 4 — Requires Approval

## Request

```yaml
target: https://api.example.com
token_ref: token-example-tester
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

The Rules of Engagement require approval before active token-acceptance testing;
the skill defers until approval is granted.

---

# Example 5 — Policy Denial

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
