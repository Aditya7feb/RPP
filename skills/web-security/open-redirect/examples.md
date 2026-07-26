# Open Redirect Examples

**File:** `skills/web-security/open-redirect/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Open Redirect
Skill. Examples illustrate the interface and outputs; they contain no implementation
code.

---

# Example 1 — Parameter-Controlled Redirect To Untrusted Origin

## Request

```yaml
target: https://app.example.com
probe_destination: https://probe.example-controlled.test
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-or-5001
    title: Redirect parameter permits redirection to an untrusted origin
    weakness: CWE-601
    risk_ref: risk-or-3001
    evidence_refs:
      - evidence-or-7001
observations:
  - id: obs-or-4001
    kind: redirect-destination-analysis
evidence:
  - id: evidence-or-7001
    observation_ref: obs-or-4001
status: completed
metrics:
  checks_performed: 4
  findings: 1
```

The `returnUrl` parameter is reflected into a `Location` header without validation,
redirecting to the benign controlled probe destination and confirming the open
redirect.

---

# Example 2 — Weak Destination Validation

## Request

```yaml
target: https://app.example.com
probe_destination: https://app.example.com.probe.example-controlled.test
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-or-5002
    title: Redirect destination validated by prefix, permitting bypass
    weakness: CWE-601
    risk_ref: risk-or-3002
    evidence_refs:
      - evidence-or-7002
status: completed
metrics:
  checks_performed: 4
  findings: 1
```

Destination validation matches the trusted host as a prefix, allowing a crafted
hostname to bypass the check.

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
- [HTTP Redirect Schema](../../../schemas/http-redirect.md)
