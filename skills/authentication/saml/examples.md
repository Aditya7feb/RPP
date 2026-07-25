# SAML Authentication Examples

**File:** `skills/authentication/saml/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the SAML
Authentication Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — Signature Wrapping Accepted

## Request

```yaml
target: https://sp.example.com/acs
assertion_ref: samlassertion-example-tester
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-saml-5001
    title: XML signature wrapping accepted by the service provider
    risk_ref: risk-saml-3001
    evidence_refs:
      - evidence-saml-7001
observations:
  - id: obs-saml-4001
    kind: signature-wrapping-analysis
evidence:
  - id: evidence-saml-7001
    observation_ref: obs-saml-4001
    redacted: true
status: completed
metrics:
  checks_performed: 7
  findings: 1
```

The service provider validates a signature on one element while consuming identity
from an attacker-injected element, indicating signature wrapping. Evidence redacts
the assertion.

---

# Example 2 — Unsigned Assertion Accepted

## Request

```yaml
target: https://sp.example.com/acs
assertion_ref: samlassertion-example-tester
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-saml-5002
    title: Unsigned assertion accepted
    risk_ref: risk-saml-3002
    evidence_refs:
      - evidence-saml-7002
status: completed
metrics:
  checks_performed: 7
  findings: 1
```

The service provider accepts an assertion with no signature, indicating signatures
are not required. Evidence redacts the assertion.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://sp.example.com/acs
assertion_ref: samlassertion-example-tester
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

The Rules of Engagement require approval before active assertion testing; the skill
defers until approval is granted.

---

# Example 4 — Policy Denial

## Request

```yaml
target: https://out-of-scope.example.net/acs
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
