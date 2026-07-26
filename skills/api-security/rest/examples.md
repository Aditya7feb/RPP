# REST API Security Examples

**File:** `skills/api-security/rest/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the REST API
Security Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — Broken Object Level Authorization

## Request

```yaml
target: https://api.example.com
identities_ref: rest-test-identities
specification_ref: api-spec-example
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-rest-5001
    title: Broken object level authorization on order resource
    weakness: CWE-639
    owasp_api: API1:2023 - Broken Object Level Authorization
    risk_ref: risk-rest-3001
    evidence_refs:
      - evidence-rest-7001
observations:
  - id: obs-rest-4001
    kind: object-authorization-analysis
evidence:
  - id: evidence-rest-7001
    observation_ref: obs-rest-4001
status: completed
metrics:
  operations_tested: 14
  findings: 1
```

The second controlled identity retrieves the first identity's order by changing the
object identifier, confirming broken object level authorization with a minimal read.

---

# Example 2 — Mass Assignment

## Request

```yaml
target: https://api.example.com
identities_ref: rest-test-identities
specification_ref: api-spec-example
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-rest-5002
    title: Mass assignment permits modifying a protected role property
    weakness: CWE-915
    owasp_api: API3:2023 - Broken Object Property Level Authorization
    risk_ref: risk-rest-3002
    evidence_refs:
      - evidence-rest-7002
status: completed
metrics:
  operations_tested: 14
  findings: 1
```

A controlled identity sets a protected property through mass assignment, confirming
broken object property level authorization.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://api.example.com
identities_ref: rest-test-identities
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

The Rules of Engagement require approval before active API authorization testing; the
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
