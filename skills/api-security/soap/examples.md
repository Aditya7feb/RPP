# SOAP API Security Examples

**File:** `skills/api-security/soap/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the SOAP API
Security Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — WS-Security Not Enforced

## Request

```yaml
target: https://api.example.com/soap
identities_ref: soap-test-identities
wsdl_ref: wsdl-example
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-soap-5001
    title: WS-Security not enforced, permitting unauthenticated processing
    weakness: CWE-306
    owasp_api: API2:2023 - Broken Authentication
    risk_ref: risk-soap-3001
    evidence_refs:
      - evidence-soap-7001
observations:
  - id: obs-soap-4001
    kind: ws-security-analysis
evidence:
  - id: evidence-soap-7001
    observation_ref: obs-soap-4001
status: completed
metrics:
  operations_tested: 7
  findings: 1
```

An operation requiring authentication is processed without WS-Security, confirming
missing message-level authentication.

---

# Example 2 — WSDL Publicly Exposed

## Request

```yaml
target: https://api.example.com/soap
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-soap-5002
    title: WSDL and operation detail publicly exposed
    weakness: CWE-200
    owasp_api: API8:2023 - Security Misconfiguration
    risk_ref: risk-soap-3002
    evidence_refs:
      - evidence-soap-7002
status: completed
metrics:
  operations_tested: 7
  findings: 1
```

The WSDL is retrievable without authentication, disclosing operation and binding
detail.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://api.example.com/soap
identities_ref: soap-test-identities
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

The Rules of Engagement require approval before active SOAP operation testing; the
skill defers until approval is granted.

---

# Example 4 — Policy Denial

## Request

```yaml
target: https://out-of-scope.example.net/soap
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
