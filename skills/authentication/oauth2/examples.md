# OAuth2 Authentication Examples

**File:** `skills/authentication/oauth2/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the OAuth2
Authentication Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — Loose Redirect URI Validation

## Request

```yaml
target: https://auth.example.com
client_credentials_ref: oauthclient-example-tester
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-oauth2-5001
    title: Redirect URI validated by prefix, permitting token leakage
    risk_ref: risk-oauth2-3001
    evidence_refs:
      - evidence-oauth2-7001
observations:
  - id: obs-oauth2-4001
    kind: redirect-uri-analysis
evidence:
  - id: evidence-oauth2-7001
    observation_ref: obs-oauth2-4001
    redacted: true
status: completed
metrics:
  checks_performed: 6
  findings: 1
```

The authorization server accepts a redirect URI matched by prefix, enabling token
leakage to an attacker-controlled path. Evidence redacts tokens.

---

# Example 2 — Missing PKCE On An Authorization Code Client

## Request

```yaml
target: https://auth.example.com
client_credentials_ref: oauthclient-example-public
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-oauth2-5002
    title: PKCE not enforced for Authorization Code client
    risk_ref: risk-oauth2-3002
    evidence_refs:
      - evidence-oauth2-7002
status: completed
metrics:
  checks_performed: 6
  findings: 1
```

A public client completes the authorization code flow without PKCE, exposing it to
code interception. PKCE SHOULD be enforced for all Authorization Code clients,
including confidential clients.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://auth.example.com
client_credentials_ref: oauthclient-example-tester
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

The Rules of Engagement require approval before active flow testing; the skill
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
- [HTTP Redirect Schema](../../../schemas/http-redirect.md)
