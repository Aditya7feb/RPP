# Content Security Policy Examples

**File:** `skills/web-security/csp/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Content
Security Policy Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — Missing Content Security Policy

## Request

```yaml
target: https://app.example.com
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-csp-5001
    title: No Content Security Policy present on sensitive responses
    weakness: CWE-693
    risk_ref: risk-csp-3001
    evidence_refs:
      - evidence-csp-7001
observations:
  - id: obs-csp-4001
    kind: policy-presence-analysis
evidence:
  - id: evidence-csp-7001
    observation_ref: obs-csp-4001
status: completed
metrics:
  checks_performed: 6
  findings: 1
```

The application serves sensitive responses without any Content Security Policy,
providing no defense-in-depth against script injection.

---

# Example 2 — Unsafe-Inline Permitted

## Request

```yaml
target: https://app.example.com
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-csp-5002
    title: script-src permits unsafe-inline, neutralizing the policy
    weakness: CWE-693
    risk_ref: risk-csp-3002
    evidence_refs:
      - evidence-csp-7002
status: completed
metrics:
  checks_performed: 6
  findings: 1
```

The `script-src` directive permits `unsafe-inline`, allowing inline script execution
and negating the policy's protection against injected scripts.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://app.example.com
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
