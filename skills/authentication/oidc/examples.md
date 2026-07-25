# OIDC Authentication Examples

**File:** `skills/authentication/oidc/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the OIDC
Authentication Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — ID Token Signature Not Validated

## Request

```yaml
target: https://id.example.com
client_credentials_ref: oidcclient-example-tester
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-oidc-5001
    title: Relying party does not validate ID token signatures
    risk_ref: risk-oidc-3001
    evidence_refs:
      - evidence-oidc-7001
observations:
  - id: obs-oidc-4001
    kind: id-token-signature-analysis
evidence:
  - id: evidence-oidc-7001
    observation_ref: obs-oidc-4001
    redacted: true
status: completed
metrics:
  checks_performed: 7
  findings: 1
```

The relying party accepts an ID token with an invalid signature, indicating
signatures are not validated. Evidence redacts the ID token.

---

# Example 2 — Missing Nonce

## Request

```yaml
target: https://id.example.com
client_credentials_ref: oidcclient-example-tester
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-oidc-5002
    title: Nonce not enforced, permitting ID token replay
    risk_ref: risk-oidc-3002
    evidence_refs:
      - evidence-oidc-7002
status: completed
metrics:
  checks_performed: 7
  findings: 1
```

The authentication request omits and does not validate a `nonce`, exposing the flow
to ID token replay.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://id.example.com
client_credentials_ref: oidcclient-example-tester
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

The Rules of Engagement require approval before active identity-flow testing; the
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
