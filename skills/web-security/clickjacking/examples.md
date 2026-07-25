# Clickjacking Examples

**File:** `skills/web-security/clickjacking/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Clickjacking
Skill. Examples illustrate the interface and outputs; they contain no implementation
code.

---

# Example 1 — Sensitive Page Without Framing Protection

## Request

```yaml
target: https://app.example.com
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-cj-5001
    title: Sensitive page framable due to missing framing protection
    weakness: CWE-1021
    risk_ref: risk-cj-3001
    evidence_refs:
      - evidence-cj-7001
observations:
  - id: obs-cj-4001
    kind: framing-control-analysis
evidence:
  - id: evidence-cj-7001
    observation_ref: obs-cj-4001
status: completed
metrics:
  checks_performed: 3
  findings: 1
```

The funds-transfer page is served without `X-Frame-Options` and without a CSP
`frame-ancestors` directive, allowing it to be framed by an untrusted origin.

---

# Example 2 — Permissive Frame-Ancestors

## Request

```yaml
target: https://app.example.com
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-cj-5002
    title: CSP frame-ancestors permits untrusted origins
    weakness: CWE-1021
    risk_ref: risk-cj-3002
    evidence_refs:
      - evidence-cj-7002
status: completed
metrics:
  checks_performed: 3
  findings: 1
```

The CSP `frame-ancestors` directive permits any origin, providing no effective
framing protection.

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
