# Server-Side Request Forgery Examples

**File:** `skills/web-security/ssrf/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Server-Side
Request Forgery Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — SSRF Confirmed Out-Of-Band

## Request

```yaml
target: https://app.example.com
collector_ref: oob-collector-controlled
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-ssrf-5001
    title: Server-side request forgery in url parameter
    weakness: CWE-918
    risk_ref: risk-ssrf-3001
    evidence_refs:
      - evidence-ssrf-7001
observations:
  - id: obs-ssrf-4001
    kind: out-of-band-analysis
evidence:
  - id: evidence-ssrf-7001
    observation_ref: obs-ssrf-4001
status: completed
metrics:
  parameters_tested: 4
  findings: 1
```

The `url` parameter causes the server to fetch the controlled collector, confirming
SSRF without reaching any internal service.

---

# Example 2 — Differential-Based SSRF Indication

## Request

```yaml
target: https://app.example.com
collector_ref: oob-collector-controlled
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-ssrf-5002
    title: Server-side fetch indicated by response differential
    weakness: CWE-918
    risk_ref: risk-ssrf-3002
    evidence_refs:
      - evidence-ssrf-7002
status: completed
metrics:
  parameters_tested: 4
  findings: 1
```

Response and timing differentials between a reachable controlled destination and an
unreachable one indicate a server-side fetch, corroborating SSRF.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://app.example.com
collector_ref: oob-collector-controlled
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

SSRF testing is high impact; the Rules of Engagement require approval, so the skill
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
- [HTTP Timing Schema](../../../schemas/http-timing.md)
