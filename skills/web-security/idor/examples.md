# Insecure Direct Object Reference Examples

**File:** `skills/web-security/idor/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Insecure Direct
Object Reference Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — Cross-Identity Object Access

## Request

```yaml
target: https://app.example.com
identities_ref: idor-test-identities
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-idor-5001
    title: Object accessible across controlled identities without authorization
    weakness: CWE-639
    risk_ref: risk-idor-3001
    evidence_refs:
      - evidence-idor-7001
observations:
  - id: obs-idor-4001
    kind: cross-identity-access-analysis
evidence:
  - id: evidence-idor-7001
    observation_ref: obs-idor-4001
status: completed
metrics:
  references_tested: 6
  findings: 1
```

The second controlled identity retrieves the first controlled identity's object by
changing the object reference, confirming missing per-object authorization with a
minimal read.

---

# Example 2 — Predictable Identifier With Missing Authorization

## Request

```yaml
target: https://app.example.com
identities_ref: idor-test-identities
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-idor-5002
    title: Predictable identifiers with absent per-object authorization
    weakness: CWE-639
    risk_ref: risk-idor-3002
    evidence_refs:
      - evidence-idor-7002
status: completed
metrics:
  references_tested: 6
  findings: 1
```

Sequential identifiers combined with absent per-object authorization allow a
controlled identity to reach an adjacent object, confirmed minimally.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://app.example.com
identities_ref: idor-test-identities
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

The Rules of Engagement require approval before cross-identity probing; the skill
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
- [Asset Schema](../../../schemas/asset.md)
