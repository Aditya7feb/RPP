# GraphQL API Security Examples

**File:** `skills/api-security/graphql/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the GraphQL API
Security Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — Introspection Enabled In Production

## Request

```yaml
target: https://api.example.com/graphql
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-gql-5001
    title: Introspection enabled in production, disclosing full schema
    weakness: CWE-200
    owasp_api: API8:2023 - Security Misconfiguration
    risk_ref: risk-gql-3001
    evidence_refs:
      - evidence-gql-7001
observations:
  - id: obs-gql-4001
    kind: introspection-analysis
evidence:
  - id: evidence-gql-7001
    observation_ref: obs-gql-4001
status: completed
metrics:
  queries_tested: 9
  findings: 1
```

The endpoint answers a standard introspection query in a production environment,
disclosing the full schema.

---

# Example 2 — Missing Depth Limit

## Request

```yaml
target: https://api.example.com/graphql
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-gql-5002
    title: Missing query depth limit enabling resource exhaustion
    weakness: CWE-770
    owasp_api: API4:2023 - Unrestricted Resource Consumption
    risk_ref: risk-gql-3002
    evidence_refs:
      - evidence-gql-7002
status: completed
metrics:
  queries_tested: 9
  findings: 1
```

A bounded, incrementally deeper probe shows the server accepts deeper nesting without
a depth limit, indicating unrestricted resource consumption. The probe remains bounded
and does not deny service.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://api.example.com/graphql
identities_ref: gql-test-identities
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

The Rules of Engagement require approval before active GraphQL probing; the skill
defers until approval is granted.

---

# Example 4 — Policy Denial

## Request

```yaml
target: https://out-of-scope.example.net/graphql
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
