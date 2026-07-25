# Mutual TLS Authentication Examples

**File:** `skills/authentication/mtls/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Mutual TLS
Authentication Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — Client Certificate Not Required

## Request

```yaml
target: https://api.example.com:8443
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-mtls-5001
    title: Service does not require a client certificate
    risk_ref: risk-mtls-3001
    evidence_refs:
      - evidence-mtls-7001
observations:
  - id: obs-mtls-4001
    kind: certificate-requirement-analysis
evidence:
  - id: evidence-mtls-7001
    observation_ref: obs-mtls-4001
    redacted: true
status: completed
metrics:
  checks_performed: 7
  findings: 1
```

A service expected to enforce mutual TLS completes a handshake without requesting a
client certificate.

---

# Example 2 — Untrusted Certificate Accepted

## Request

```yaml
target: https://api.example.com:8443
client_certificate_ref: clientcert-example-tester
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-mtls-5002
    title: Self-signed client certificate accepted
    risk_ref: risk-mtls-3002
    evidence_refs:
      - evidence-mtls-7002
status: completed
metrics:
  checks_performed: 7
  findings: 1
```

The service accepts a self-signed client certificate, indicating weak client-chain
validation. Evidence redacts key material.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://api.example.com:8443
client_certificate_ref: clientcert-example-tester
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

The Rules of Engagement require approval before active mutual TLS testing; the skill
defers until approval is granted.

---

# Example 4 — Policy Denial

## Request

```yaml
target: https://out-of-scope.example.net:8443
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
- [Certificate Schema](../../../schemas/certificate.md)
